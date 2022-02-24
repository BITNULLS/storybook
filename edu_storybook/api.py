"""
api.py
    Contains all the API endpoints.

Routes:
    /api/
    /api/login
    /api/logout
    /api/register
    /api/password/forgot
    /api/password/reset
    /api/admin/book/download
    /api/admin/book/upload
    /api/admin/book/grant
    /api/admin/page
    /api/admin/download/user
    /api/admin/download/action
    /api/admin/get/user
    /api/quiz/submit
    /api/storyboard/page/<int:book_id_in>/<int:page_number_in>
    /api/storyboard/action
"""

from flask import request
from flask import make_response
from flask import Blueprint
from flask import send_file

from pdf2image import convert_from_path
import os
import csv
import uuid
import jwt
import hashlib
import cx_Oracle
import random
import string
import datetime
import bcrypt

from core.auth import validate_login, issue_auth_token
from core.bucket import bucket
from core.helper import allowed_file, label_results_from
from core.email import send_email
from core.config import config
from core.db import connection, conn_lock
from core.sensitive import jwt_key
from core.remove_watchdog import future_del_temp
from core.reg_exps import *

api = Blueprint('api', __name__)

@api.route("/api/")
def api_index():
    # revalidate login
    if 'Authorization' in request.cookies:
        # check if a user has valid credentials
        auth = request.cookies.get('Authorization')
        vl = validate_login(
            auth,
            permission=0
        )
        if vl != True:
            return vl

        res = make_response({
            "status": "ok",
            "login": "reverified"
        })
        issue_auth_token(res, auth)
        return res
    return {
        "status": "ok"
    }

@api.route("/api/login")
def login(email: str, password: str):
    # check that all expected inputs are received
    try:
        assert 'email' in request.form
        assert 'password' in request.form
    except AssertionError:
        return {
            "status": "fail",
            "fail_no": 1,
            "message": "Either the email or the password was not provided."
        }, 400, {"Content-Type": "application/json"}

    # sanitize inputs: make sure they're all alphanumeric, longer than 8 chars
    if re_email.match(request.form['email']) is None or \
            re_alphanumeric8.match(request.form['password']) is None:
        return {
            "status": "fail",
            "fail_no": 2,
            "message": "Either the email or the password failed a sanitize check. The POSTed fields should be alphanumeric, longer than 8 characters."
        }, 400, {"Content-Type": "application/json"}

    # all good, now query database
    email = (request.form['email']).lower().strip()

    cursor = connection.cursor()
    try:
        cursor.execute(
            "select * from USER_PROFILE where email='" + email + "'"
        )
        label_results_from(cursor)
    except cx_Oracle.Error as e:
        return {
            "status": "fail",
            "fail_no": 3,
            "message": "Error when querying database.",
            "database_message": str(e)
        }, 400, {"Content-Type": "application/json"}

    result = cursor.fetchone()
    if result is None:
        return {
            "status": "fail",
            "fail_no": 4,
            "message": "No email matches what was passed."
        }, 400, {"Content-Type": "application/json"}

    # print(result)
    # print(result[8])
    if not bcrypt.checkpw(request.form['password'].encode('utf8'), result['PASSWORD'].encode('utf8')):
        return {
            "status": "fail",
            "fail_no": 5,
            "message": "Password is incorrect."
        }, 400, {"Content-Type": "application/json"}

    user_id = result['USER_ID']
    session_id = str(uuid.uuid4())  # generate a unique token for a user

    try:
        conn_lock.acquire()
        cursor.execute(
            "update USER_SESSION set session_id='" + session_id +
            "', active=1 where user_id='" + str(user_id) + "'"
        )
        connection.commit()
    except cx_Oracle.Error as e:
        return {
            "status": "fail",
            "fail_no": 6,
            "message": "Error when updating database.",
            "database_message": str(e)
        }, 400, {"Content-Type": "application/json"}
    finally:
        conn_lock.release()

    iat = int(time.time())

    res = make_response({
        "status": "ok",
        "message": "Successfully authenticated",
        "iat": iat
    })
    token = jwt.encode({
        "iat": iat,
        "session": session_id,
        "sub": user_id,
        "permission": result['ADMIN']
    }, jwt_key, algorithm=config['jwt_alg'])
    res.set_cookie(
        "Authorization",
        "Bearer " + token,
        max_age=config["login_duration"],
        # domain=domain_name#, # TODO: uncomment in production
        # secure=True,
        # httponly=True
    )

    try:
        conn_lock.acquire()
        cursor.execute(
            "update USER_PROFILE set LAST_LOGIN=CURRENT_TIMESTAMP where user_id='" +
            str(user_id) + "'"
        )
        connection.commit()
    except cx_Oracle.Error as e:
        return {
            "status": "fail",
            "fail_no": 7,
            "message": "Error when updating database.",
            "database_message": str(e)
        }, 400, {"Content-Type": "application/json"}
    finally:
        conn_lock.release()

    return res

@api.route("/api/logout")
def logout(auth):
    # make sure the user is authenticated first
    auth = request.cookies.get('Authorization')
    vl = validate_login(
        auth,
        permission=0
    )
    if vl != True:
        return vl

    if 'Bearer ' in auth:
        auth = auth.replace('Bearer ', '', 1)
    token = jwt.decode(auth, jwt_key, algorithms=config['jwt_alg'])

    cursor = connection.cursor()
    try:
        conn_lock.acquire()
        cursor.execute(
            "update USER_SESSION set active=0 where user_id='" +
            token['sub'] + "'"
        )
        connection.commit()
    except cx_Oracle.Error as e:
        return {
            "status": "fail",
            "fail_no": 8,
            "message": "Error when updating database.",
            "database_message": str(e)
        }
    finally:
        conn_lock.release()

    res = make_response({
        "status": "ok"
    })
    res.set_cookie('Authorization', '', expires=0)
    return res

@api.route("/api/register")
def register(email: str, password: str, first_name: str, last_name: str, school_id: int):
    # check that all expected inputs are not empty
    try:
        assert len('email') > 0
        assert len('password') > 0
        assert len('first_name') > 0
        assert len('last_name') > 0
        assert len('school_id') > 0
    except AssertionError:
        return {
            "status": "fail",
            "fail_no": 1,
            "message": "A field was not provided"
        }

    # sanitize inputs: make sure they're all alphanumeric, longer than 8 chars
    if re_email.match(request.form['email']) is None or \
            re_alphanumeric8.match(request.form['password']) is None or \
            re_alphanumeric2.match(request.form['first_name']) is None or \
            re_alphanumeric2.match(request.form['last_name']) is None:
        return {
            "status": "fail",
            "fail_no": 2,
            "message": "Some field failed a sanitize check. The POSTed fields should be alphanumeric, longer than 8 characters."
        }

    # all good, now query database
    email = (email).lower().strip()
    first_name = (first_name).strip()
    last_name = (last_name).strip()
    school_id = (school_id).lower().strip()

    cursor = connection.cursor()
    try:
        cursor.execute(
            "select * from USER_PROFILE where email='" + email + "'"
        )
    except cx_Oracle.Error as e:
        return {
            "status": "fail",
            "fail_no": 3,
            "message": "Error when querying database.",
            "database_message": str(e)
        }

    result = cursor.fetchone()
    if result is not None:
        return {
            "status": "fail",
            "fail_no": 4,
            "message": "Email is Already Registered."
        }

    hashed = bcrypt.hashpw(
        request.form['password'].encode('utf8'), bcrypt.gensalt())

    try:
        conn_lock.acquire()
        cursor.execute(
            "INSERT into USER_PROFILE (email, first_name, last_name, admin, school_id, study_id, password) VALUES ('"
            + email + "', '"
            + first_name + "', '"
            + last_name + "', "
            + "0 , "
            + school_id + ", "
            + 'null' + ", '"
            + hashed.decode('utf8')
            + "')"
        )
        connection.commit()
    except cx_Oracle.Error as e:
        return {
            "status": "fail",
            "fail_no": 5,
            "message": "Error when querying database.",
            "database_message": str(e)
        }
    finally:
        conn_lock.release()

        send_email(first_name + last_name, email, 'Edu Storybooks', 'edustorybooks@gmail.com',
                   'Welcome to Edu Storybooks', 'Dear ' + first_name + ' ' + last_name + ',' +
                   '\n\nThanks for registering an account with Edu Storybooks! :)')
    return {
        "status": "ok"
    }


# input email & check if email exists
@api.route("/api/password/forgot", methods=['POST'])
def password_forgot():

    # checks for input
    try:
        assert 'email' in request.form
    except AssertionError:
        return {
            "status": "fail",
            "fail_no": 1,
            "message": "Email was not provided."
        }, 400, {"Content-Type": "application/json"}

    # sanitize inputs: alphanumeric, > 8 chars
    if re_email.match(request.form['email']) is None:
        return {
            "status": "fail",
            "fail_no": 2,
            "message": "Email failed sanitization check of more than 8 characters &/or alphanumeric."
        }, 400, {"Content-Type": "application/json"}

    # begin querying database
    email = (request.form['email']).lower().strip()

    # create random sequence of 512 byte string
    rand_str = ''.join(random.SystemRandom().choice(
        string.ascii_uppercase + string.digits) for _ in range(512))

    cursor = connection.cursor()
    try:
        cursor.execute(
            # fix the SQL statement with user_session?
            "SELECT * FROM USER_PROFILE WHERE EMAIL ='" + email + "'")
    except cx_Oracle.Error as e:
        return {
            "status": "fail",
            "fail_no": 3,
            "message": "Error when querying database.",
            "database_message": str(e)
        }, 400, {"Content-Type": "application/json"}

    result = cursor.fetchone()
    if result is None:
        return {
            "status": "fail",
            "fail_no": 4,
            "message": "No email matches what was passed."
        }, 400, {"Content-Type": "application/json"}

    user_id = result[9]
    user_name = result[1] + ' ' + result[2]

    now = datetime.datetime.now()
    req_date = (now.strftime("%Y/%m/%d"))

    try:  # it does not insert with Oracle db? (but works in SQLDeveloper)
        conn_lock.acquire()
        cursor.execute(
            "INSERT INTO PASSWORD_RESET(USER_ID, RESET_KEY, REQUEST_DATE) VALUES('" + user_id + "','" + rand_str + "', TO_DATE('" + req_date + "', 'yyyy/mm/dd'))")
        connection.commit()
    except cx_Oracle.Error as e:
        return {
            "status": "fail",
            "fail_no": 5,
            "message": "Error when querying database.",
            "database_message": str(e)
        }, 400, {"Content-Type": "application/json"}
    finally:
        conn_lock.release()

    key = 'edustorybook.com/Password/Reset#key=' + rand_str

    send_email(user_name, email, 'Edu Storybooks',
               'edustorybooks@gmail.com', 'Password Reset Request', key)

    return {
        "status": "ok"
    }


# new password updates old password in USER_PROFILE & deletes the inserted row in PASSWORD_RESET
# check if both password fields match
@api.route("/api/password/reset", methods=['POST'])
def password_reset():
   # check expected input
    try:
        assert 'new_pass' in request.form
        assert 'confirm_pass' in request.form
        assert 'reset_key' in request.form
    except AssertionError:
        return {
            "status": "fail",
            "fail_no": 1,
            "message": "Either password was not provided."
        }, 400, {"Content-Type": "application/json"}

    # sanitize inputs: make sure they're all alphanumeric, longer than 8 chars
    if re_alphanumeric8.match(request.form['new_pass']) is None or \
            re_alphanumeric8.match(request.form['confirm_pass']) is None:
        return {
            "status": "fail",
            "fail_no": 2,
            "message": "Either one or both passwords failed sanitization check of more than 8 characters &/or alphanumeric."
        }, 400, {"Content-Type": "application/json"}

    # check if both passwords match
    if (request.form['new_pass'] != request.form['confirm_pass']):
        return {
            "status": "fail",
            "fail_no": 3,
            "message": "Both passwords do not match."
        }, 400, {"Content-Type": "application/json"}

    hashed = bcrypt.hashpw(
        request.form['confirm_pass'].encode('utf8'), bcrypt.gensalt())

    reset_key = (request.form['reset_key'])

    # connect to database
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT USER_ID FROM PASSWORD_RESET WHERE RESET_KEY ='" + reset_key + "'")

    except cx_Oracle.Error as e:
        return {
            "status": "fail",
            "fail_no": 4,
            "message": "Error when querying database.",
            "database_message": str(e)
        }, 400, {"Content-Type": "application/json"}

    result = cursor.fetchone()
    if result is None:
        return {
            "status": "fail",
            "fail_no": 5,
            "message": "No reset_key matches what was passed."
        }, 400, {"Content-Type": "application/json"}

    try:
        conn_lock.acquire()
        cursor.execute("UPDATE USER_PROFILE set PASSWORD ='" +
                       hashed.decode('utf8') + "' WHERE user_id ='" + result[0] + "'")
        connection.commit()
    except cx_Oracle.Error as e:
        return {
            "status": "fail",
            "fail_no": 6,
            "message": "Error when querying database.",
            "database_message": str(e)
        }, 400, {"Content-Type": "application/json"}
    finally:
        conn_lock.release()

    try:
        conn_lock.acquire()
        cursor.execute(
            "DELETE FROM PASSWORD_RESET WHERE RESET_KEY ='" + reset_key + "'")
        connection.commit()
    except cx_Oracle.Error as e:
        return {
            "status": "fail",
            "fail_no": 7,
            "message": "Error when querying database.",
            "database_message": str(e)
        }, 400, {"Content-Type": "application/json"}
    finally:
        conn_lock.release()

    return {
        "status": "ok"
    }


@api.route("/api/admin/book/download", methods=['POST'])
def admin_download_book():

    # validate that user has admin rights to download books
    auth = request.cookies.get('Authorization')
    vl = validate_login(
        auth,
        permission=0
    )
    if vl != True:
        return vl

    # get file name from request
    fileInput = request.form['filename']
    try:
        # download file to bucket
        filepath = bucket.download_bucket_file(fileInput)
        # send file back
        return send_file(filepath)
    except:
        return {
            "status": "fail",
            "fail_no": 14,
            "message": "could not download file"
        }, 400, {"Content-Type": "application/json"}


@api.route("/api/admin/book/upload", methods=['POST'])
def admin_book_upload():

    # validate that user has admin rights to upload books
    auth = request.cookies.get('Authorization')
    vl = validate_login(
        auth,
        permission=0
    )
    if vl != True:
        return vl

    # get parameters for adding to book table
    book_name = (request.form.get('book_name')).lower().strip()
    book_description = (request.form.get('book_description')).lower().strip()
    # book_id and created_on handled by trigger

    # check that study_id and page_count are ints
    try:
        study_id = int(request.form['study_id'])
    except ValueError:
        return {
            "status": "fail",
            "fail_no": 2,
            "message": "study_id failed a sanitize check. The POSTed field should be an integer."
        }, 400, {"Content-Type": "application/json"}

    # check if the post request has the file part
    if 'file' not in request.files:
        return {
            "status": "fail",
            "fail_no": 10,
            "message": "no file selected"
        }, 400, {"Content-Type": "application/json"}

    # get file from request files
    file = request.files['file']

    if file.filename == '':
        return {
            "status": "fail",
            "fail_no": 11,
            "message": "filename is empty string"
        }, 400, {"Content-Type": "application/json"}

    if file and allowed_file(file.filename):

        # prepend unique uuid for filename
        filename = str(uuid.uuid4()) + "_" + file.filename

        # save file to local /temp/file_upload folder
        filePath = os.path.join("temp/", filename)
        filePath = filePath.replace('\\', '/')
        file.save(filePath)

        # convert pdf to images
        book_pngs = convert_from_path("temp/" + filename, 500)

        # remove pdf from temp/file_upload. we don't need it anymore
        os.remove("temp/" + filename)

        # remove .pdf extension from filename
        filename = filename.rstrip(".pdf")

        # make folder to store images
        os.makedirs("temp/" + filename + "_images")

        # 1) insert files into bucket
        try:
            # iterate through length of book
            for i in range(len(book_pngs)):
                # Save pages as images in the pdf

                book_pngs[i].save('temp/'+ filename + "_images/" + filename + "_" + str(i+1) +'.png', 'PNG')
                # upload images to a folder in bucket
                bucket.upload_bucket_file('temp/'+ filename + "_images/" + filename + "_" + str(i+1) +'.png', filename + "_images/" + filename + "_" + str(i+1) +'.png')
                # remove img file
                os.remove('temp/'+ filename + "_images/" + filename + "_" + str(i+1) +'.png')

            # remove temp dir
            os.rmdir("temp/" + filename + "_images")

            return {
                "status": "ok",
                "message": "file(s) uploaded"
            }

        except Exception as e:
            return {
                "status": "fail",
                "fail_no": 12,
                "message": "Error when trying to upload file.",
                "flask_message": str(e)
            }, 400, {"Content-Type": "application/json"}

        # connect to database
        cursor = connection.cursor()

        # 2) insert book into table
        try:
            conn_lock.acquire()

            cursor.execute("INSERT into BOOK (book_name, description, study_id, folder, page_count) VALUES ('"
                           + book_name + "', '"
                           + book_description + "', '"
                           + str(study_id) + "', '"
                           + filename + "', "
                           + str(len(book_pngs)) + ")")
            # commit to database
            connection.commit()

        except cx_Oracle.Error as e:
            return {
                "status": "fail",
                "fail_no": 4,
                "message": "Error when querying database. 1159",
                "database_message": str(e)
            }
        finally:
            conn_lock.release()

        return {
            "status": "ok",
        }

    return {
        "status": "fail",
        "fail_no": 13,
        "message": "invalid file format or file"
    }, 400, {"Content-Type": "application/json"}


@api.route("/api/admin/book/grant", methods=['POST'])
def admin_add_book_to_study():

    # validate that user can access data
    auth = request.cookies.get('Authorization')
    vl = validate_login(
        auth,
        permission=0
    )
    if vl != True:
        return vl

    # get parameters
    book_name = (request.form.get('book_name')).lower().strip()
    book_url = (request.form.get('book_url')).lower().strip()
    book_description = (request.form.get('book_description')).lower().strip()
    study_id = (request.form.get('study_id'))
    # book_id and created_on handled by trigger

    # connect to database
    cursor = connection.cursor()

    # insert query
    try:
        conn_lock.acquire()
        cursor.execute("INSERT into BOOK (book_name, url, description, study_id) VALUES ('"
                       + book_name + "', '"
                       + book_url + "', '"
                       + book_description + "', "
                       + study_id
                       + ")"
                       )
        # commit to database
        connection.commit()

    except cx_Oracle.Error as e:
        return {
            "status": "fail",
            "fail_no": 4,
            "message": "Error when querying database.",
            "database_message": str(e)
        }
    finally:
        conn_lock.release()


@api.route("/api/admin/page", methods=['POST', 'GET', 'PUT', 'DELETE'])
def admin_page_handler():
    """
    This endpoint handles quiz questions and answers
    """
    auth = request.cookies.get('Authorization')
    vl = validate_login(
        auth,
        permission=1
    )
    if vl != True:
        return vl

    if 'Bearer ' in auth:
        auth = auth.replace('Bearer ', '', 1)
    token = jwt.decode(auth, jwt_key, algorithms=config['jwt_alg'])

    if request.method == 'POST':
        # check to make sure you have a book_id
        try:
            assert 'book_id_in' in request.form
            assert 'school_id_in' in request.form
            assert 'question_in' in request.form
            assert 'page_prev_in' in request.form
            assert 'page_next_in' in request.form
            assert 'answers_in' in request.form

        except AssertionError:
            return {
                "status": "fail",
                "fail_no": 1,
                "message": "book_id_in, school_id_in, question_in, page_prev_in, page_next_in, or answers_in not provided"
            }, 400, {"Content-Type": "application/json"}

        # sanitize inputs: check ints
        try:
            
            book_id_in = int(request.form['book_id_in'])
            school_id_in = int(request.form['school_id_in'])
            page_prev_in = int(request.form['page_prev_in'])
            page_next_in = int(request.form['page_next_in'])

        except ValueError:
            return {
                "status": "fail",
                "fail_no": 2,
                "message": "book_id_in, school_id_in, page_prev_in, or  page_next_in failed a sanitize check. The posted fields should be integers."
            }, 400, {"Content-Type": "application/json"}

        # not sanitizing questions or answers. may have any text since its up to the customer's discretion what the question is
        # regex is not very efficient method here for sql injection check

        cursor = connection.cursor()

        try:
            conn_lock.acquire()
            cursor.callproc("insert_question_proc",\
                [request.form['question_in'],\
                    request.form['school_id_in'],\
                    request.form['book_id_in'],\
                    request.form['page_prev_in'],\
                    request.form['page_next_in'],\
                    request.form['answers_in']])
                
            # commit changes to db
            connection.commit()

        except cx_Oracle.Error as e:
            return {
                "status": "fail",
                "fail_no": 3,
                "message": "Error when querying database. line 889",
                "database_message": str(e)
            }, 400, {"Content-Type": "application/json"}
        
        finally:
            conn_lock.release()

        return {
          "status": "ok"
        }

    elif request.method == 'GET':  # Get = get (retrieve pages)
        cursor = connection.cursor()
        
        # check to make sure you have a book_id
        try:
            assert 'book_id' in request.form
        except AssertionError:
            return {
                "status": "fail",
                "fail_no": 1,
                "message": "book_id was not provided."
            }, 400, {"Content-Type": "application/json"}

        try:
            book_id = int(request.form['book_id'])
        except ValueError:
            return {
                "status": "fail",
                "fail_no": 2,
                "message": "book_id failed a sanitize check. The POSTed field should be an integer."
            }, 400, {"Content-Type": "application/json"}

        try:
            conn_lock.acquire()
            cursor.execute(
                "SELECT QUESTION.QUESTION_ID, QUESTION.QUESTION, ANSWER.ANSWER FROM QUESTION " +
                "INNER JOIN USER_RESPONSE ON USER_RESPONSE.QUESTION_ID = QUESTION.QUESTION_ID " +
                "INNER JOIN ANSWER ON USER_RESPONSE.QUESTION_ID = ANSWER.QUESTION_ID " +
                "WHERE BOOK_ID=" + request.form["book_id"]
            )
            label_results_from(cursor)

        except cx_Oracle.Error as e:
            return {
                "status": "fail",
                "fail_no": 3,
                "message": "Error when querying database.",
                "database_message": str(e)
            }, 400, {"Content-Type": "application/json"}
        finally:
            conn_lock.release()
        

        # fetching all the questions and storing them in questions array
        questions = []

        while True:
            result = cursor.fetchone()
            if result is None:
                break
            questions.append(result)
        if len(questions) == 0:
            return {
                "status": "fail",
                "fail_no": 4,
                "message": "No book_id matches what was passed."
            }, 400, {"Content-Type": "application/json"}
        return {
            "status": "ok",
            "questions": questions
        }

    elif request.method == 'PUT':
        # check correct inputs
        try:
            assert 'question_id_in' in request.form
            assert 'question_in' in request.form
            assert 'answers_in' in request.form

        except AssertionError:
            return {
                "status": "fail",
                "fail_no": 1,
                "message": "question_id_in, question_in, or answers_in not provided"
            }, 400, {"Content-Type": "application/json"}

        # check that question id is an int
        try:
            question_id = int(request.form['question_id_in'])

        except ValueError:
            return {
                "status": "fail",
                "fail_no": 2,
                "message": "question_id failed a sanitize check. The POSTed field should be an integer."
            }, 400, {"Content-Type": "application/json"}

        # try query calling procedure "edit_question_proc"
        cursor = connection.cursor()
        try:
            conn_lock.acquire()
            cursor.callproc("edit_question_proc",\
                [request.form['question_id_in'],\
                    request.form['question_in'],\
                    request.form['answers_in']])
                
            # commit changes to db
            connection.commit()

        except cx_Oracle.Error as e:
            return {
                "status": "fail",
                "fail_no": 3,
                "message": "Error when querying database. line 889",
                "database_message": str(e)
            }, 400, {"Content-Type": "application/json"}

        finally:
            conn_lock.release()

        return {
          "status": "ok"
        }

    elif request.method == 'DELETE':  # DELETE = delete a page
        try:
            question_id_in = int(request.form['question_id_in'])

        except ValueError:
            return {
                "status": "fail",
                "fail_no": 2,
                "message": "question_id_in failed a sanitize check. The posted field should be an integer."
            }, 400, {"Content-Type": "application/json"}

        cursor = connection.cursor()

        try:
            cursor.callproc('delete_question_answer_proc', [
                            request.form['question_id_in']])

            connection.commit()

        except cx_Oracle.Error as e:
            return {
                "status": "fail",
                "fail_no": 4,
                "message": "Error when querying database.",
                "database_message": str(e)
            }

        return {
            "status": "ok"
        }

    else:
        return "Invalid Operation"


@api.route("/api/admin/download/user", methods=['POST'])
def admin_download_user_data():
    """
    Exports user profile data to a csv file

    - Connects to database
    - Computes a select query to get user profile data
    - calls create_csv(query_results, headers) to create csv-formatted string
    - creates and returns csv file using csv-formatted string
    """
    # validate that user can access data
    auth = request.cookies.get('Authorization')
    vl = validate_login(
        auth,
        permission=0
    )
    if vl != True:
        return vl

    # connect to database
    cursor = connection.cursor()

    # select query
    try:
        cursor.execute("select\
        user_profile.email, \
        user_profile.first_name, \
        user_profile.last_name, \
        user_profile.created_on, \
        user_profile.last_login, \
        school.school_name, \
        study.study_name from user_profile \
        inner join school on user_profile.school_id = school.school_id \
        inner join study on user_profile.study_id = study.study_id")

    except cx_Oracle.Error as e:
        return {
            "status": "fail",
            "fail_no": 4,
            "message": "Error when querying database.",
            "database_message": str(e)
        }

    # assign variable data to cursor.fetchall(). if i do not assign it to a variable, Response() sees it as an empty string
    data = cursor.fetchall()

    # column headers for csv
    headers = [
        "Username",
        "Email",
        "First Name",
        "Last Name",
        "Created On",
        "Last Login",
        "School"
    ]

    # create filename with unique guid to prevent duplicates
    filename = "temp/csv_export_" + str(uuid.uuid4()) + ".csv"

    # write data to new csv file in data/csv_exports
    with open(filename, "w", newline="") as csvfile:
        # init csv writer
        writer = csv.writer(csvfile)
        # add headers
        writer.writerow(headers)
        # iterate through data -> data is a list of tuples
        for row in list(map(lambda x: tuple(map(lambda i: str(i), x)), data)):
            writer.writerow(row)

    # calculate etag for cloudflare
    sha1 = hashlib.sha1()
    with open(filename, 'rb') as f:
        while True:
            data = f.read(config['buffer_size'])
            if not data:
                break
            sha1.update(data)

    # queue the file to be removed
    future_del_temp(filename)

    try:
        # return response
        return send_file(filename, mimetype="text/csv", attachment_filename="user.csv", as_attachment=True, etag=sha1.hexdigest())
    except Exception as e:
        return {
            "status": "fail",
            "fail_no": 9,
            "message": "Error when sending csv file.",
            "flask_message": str(e)
        }


@api.route("/api/admin/download/action", methods=['POST'])
def admin_download_action_data():
    """
    Exports user action data to a csv file

    - Connects to database
    - Computes a select query to get user profile data
    - calls create_csv(query_results, headers) to create csv-formatted string
    - creates and returns csv file using csv-formatted string
    """
    # validate that user can access data
    auth = request.cookies.get('Authorization')
    vl = validate_login(
        auth,
        permission=0
    )
    if vl != True:
        return vl

    # connect to database
    cursor = connection.cursor()

    # select query
    try:
        cursor.execute("select user_profile.email, \
        action.action_start, \
        action.action_stop, \
        book.book_name, \
        action_key.action_name, \
        action_detail.detail_description \
        from user_profile \
        inner join action on user_profile.user_id = action.user_id \
        inner join book on action.book_id = book.book_id \
        inner join action_detail on action_detail.detail_id = action.detail_id \
        inner join action_key on action_detail.action_id = action_key.action_id")

    except cx_Oracle.Error as e:
        return {
            "status": "fail",
            "fail_no": 4,
            "message": "Error when querying database.",
            "database_message": str(e)
        }

    # assign variable data to cursor.fetchall(). if i do not assign it to a variable, Response() sees it as an empty string
    data = cursor.fetchall()

    # column headers for csv
    headers = [
        "Email",
        "Start",
        "Stop",
        "Book Name",
        "Action",
        "Details"
    ]

    # create filename with unique guid to prevent duplicates
    filename = "temp/csv_export_" + str(uuid.uuid4()) + ".csv"

    # write data to new csv file in data/csv_exports
    with open(filename, 'w', newline='') as csvfile:
        # init csv writer
        writer = csv.writer(csvfile)
        # add headers
        writer.writerow(headers)
        # iterate through data -> data is a list of tuples
        for row in list(map(lambda x: tuple(map(lambda i: str(i), x)), data)):
            writer.writerow(row)

    # calculate etag
    sha1 = hashlib.sha1()
    with open(filename, 'rb') as f:
        while True:
            data = f.read(config['buffer_size'])
            if not data:
                break
            sha1.update(data)

    # queue the file to be removed
    future_del_temp(filename)

    try:
        # return response
        return send_file(filename, mimetype="text/csv", attachment_filename="action.csv", as_attachment=True, etag=sha1.hexdigest())
    except Exception as e:
        return {
            "status": "fail",
            "fail_no": 9,
            "message": "Error when sending csv file.",
            "flask_message": str(e)
        }


# take in input param ofset that will be the limit of 50 ofset of 50 and then be happy.
@api.route("/api/admin/get/user", methods=['GET'])
def admin_get_users():
    """
    Exports user data to a json

    - Connects to database
    - Computes a select query to get user data
    - return USER_ID, USERNAME (full), STUDY that they currently belong to. 
        Important: Sort by join date, or login date, or something. We want fresh users first.
    - Allow an admin to retrieve a JSON list of all of the users. 
        LIMIT the response to only 50 rows, and use the PL/SQL OFFSET to offset to grab the first 50 rows, then next 50 rows. 
        Make offset an input parameter (int).
    """

    # validate that user has rights to access books
    auth = request.cookies.get('Authorization')
    vl = validate_login(
        auth,
        permission=1
    )
    if vl != True:
        return vl

    if 'Bearer ' in auth:
        auth = auth.replace('Bearer ', '', 1)

    token = jwt.decode(auth, jwt_key, algorithms=config['jwt_alg'])

    # check to make sure you have a offset
    try:
        assert 'offset' in request.form
    except AssertionError:
        return {
            "status": "fail",
            "fail_no": 1,
            "message": "offset was not provided."
        }, 400, {"Content-Type": "application/json"}

    # sanitize inputs: make sure offset is int
    try:
        offset = int(request.form['offset'])
    except ValueError:
        return {
            "status": "fail",
            "fail_no": 2,
            "message": "offset failed a sanitize check. The POSTed field should be an integer."
        }, 400, {"Content-Type": "application/json"}

    # connect to database
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT USER_ID, EMAIL, STUDY_ID FROM USER_PROFILE ORDER BY CREATED_ON DESC OFFSET " +
            request.form["offset"] + " ROWS FETCH NEXT 50 ROWS ONLY"
        )
        label_results_from(cursor)
    except cx_Oracle.Error as e:
        return {
            "status": "fail",
            "fail_no": 3,
            "message": "Error when accessing database.",
            "database_message": str(e)
        }, 400, {"Content-Type": "application/json"}

    users = cursor.fetchall()

    return {
        "status": "ok",
        "users": users
    }

@api.route("/api/quiz/submit", methods=['POST'])
def quiz_submit_answer():
    try:
        assert 'answer_id' in request.form
        assert 'question_id' in request.form
    except AssertionError:
        return {
            "status": "fail",
            "fail_no": 4,
            "message": "Either the answer_id or the question_id was not provided."
        }, 400, {"Content-Type": "application/json"}

    try:
        answer_id = int(request.form['answer_id'])
        question_id = int(request.form['question_id'])
    except ValueError:
        return {
            "status": "fail",
            "fail_no": 5,
            "message": "Either the answer_id or the question_id contained invalid characters."
        }, 400, {"Content-Type": "application/json"}

    # make sure the user is authenticated first
    auth = request.cookies.get('Authorization')
    vl = validate_login(
        auth,
        permission=0
    )
    if vl != True:
        return vl

    if 'Bearer ' in auth:
        auth = auth.replace('Bearer ', '', 1)
    token = jwt.decode(auth, jwt_key, algorithms=config['jwt_alg'])

    cursor = connection.cursor()
    try:
        conn_lock.acquire()
        cursor.execute(
            "insert into user_response (user_id, question_id, answer_id, answered_on) values (" + "'" +
            token['sub'] + "', " + str(question_id) +
            ", " + str(answer_id) + ", current_timestamp)"
        )
        connection.commit()
    except cx_Oracle.Error as e:
        return {
            "status": "fail",
            "fail_no": 6,
            "message": "Error when updating database.",
            "database_message": str(e)
        }, 400, {"Content-Type": "application/json"}
    finally:
        conn_lock.release()

    return {"status": "ok"}


@api.route("/api/storyboard/page/<int:book_id_in>/<int:page_number_in>", methods=['GET'])
def storyboard_get_page(book_id_in, page_number_in):
    # make sure user is authenticated
    auth = request.cookies.get('Authorization')
    vl = validate_login(
        auth,
        permission=0
    )
    if vl != True:
        return vl

    if 'Bearer' in auth:
        auth = auth.replace('Bearer ', '', 1)

    token = jwt.decode(auth, jwt_key, algorithms=config['jwt_alg'])

    # sanitize inputs: make sure book_id, page_number are ints
    try:
        book_id = int( book_id_in)
        page_number = int(page_number_in)
    except ValueError:
        return {
            "status": "fail",
            "fail_no": 2,
            "message": "The book_id or page_number failed a sanitize check. The POSTed fields should be an integer."
        }, 400, {"Content-Type": "application/json"}

    # goes into database and gets the bucket folder.
    # goes into bucket and then says I want this image from this folder.
    cursor = connection.cursor()

    try:
        # get folder that holds that book's images
        cursor.execute(
            "SELECT folder FROM BOOK where book_id =" + str(book_id))
    except cx_Oracle.Error as e:
        return {"status": "fail",
                "fail_no": 3,
                "message": "Error when updating database action",
                "database_message": str(e)
                }, 400, {"Content-Type": "application/json"}

    # check if this is in write format ; then we have to fix it and ammend it with page number
    fileInput = cursor.fetchone()[0]
    fileInput = fileInput + '/' + fileInput + '_' + str(page_number) + '.png'

    try:
        return send_file(bucket.download_bucket_file(fileInput))
    except:
        return {
            "status": "fail",
            "fail_no": 4,
            "message": "could not get image"
        }, 400, {"Content-Type": "application/json"}


@api.route("/api/storyboard/action", methods=['POST'])
def storyboard_save_user_action():
    '''
    Code the storyboard_save_user_action() function in the same style as logout()
    Screenshot a successful POST request to the /storyboard/action endpoint.
    Add to the backend/API.md the relevant documentation for the /storyboard/action endpoint
    in the same style as the login/ endpoint documentation.
    '''
    # make sure user is authenticated
    auth = request.cookies.get('Authorization')
    vl = validate_login(
        auth,
        permission=0
    )
    if vl != True:
        return vl

    if 'Bearer' in auth:
        auth = auth.replace('Bearer ', '', 1)

    token = jwt.decode(auth, jwt_key, algorithms=config['jwt_alg'])

    # check that all expected inputs are received
    try:
        assert 'book_id' in request.form
        assert 'detail_description' in request.form
        assert 'action_key_id' in request.form
        assert 'action_start' in request.form
        assert 'action_stop' in request.form
    except AssertionError:
        return {
            "status": "fail",
            "fail_no": 1,
            "message": "Either the book_id, detail_description, or action_id was not provided."
        }, 400, {"Content-Type": "application/json"}

    # sanitize inputs: make sure book_id, action_key_id are ints
    try:
        book_id = int(request.form["book_id"])
        action_key_id = int(request.form["action_key_id"])
    except ValueError:
        return {
            "status": "fail",
            "fail_no": 2,
            "message": "The book_id or action_key_id failed a sanitize check. The POSTed fields should be an integer for book_id or action_id."
        }, 400, {"Content-Type": "application/json"}

    # sanitize inputs: make sure action_start and action_stop are in correct format
    if re_timestamp.match(request.form["action_start"]) is None or \
            re_timestamp.match(request.form["action_stop"]) is None or \
            re_alphanumeric.match(request.form["detail_description"]) is None:
        return {
            "status": "fail",
            "fail_no": 3,
            "message": "Either the action_start, action_stop, or detail_description failed a sanitize check. The POSTed fields should be in date format YYYY-MM-DD HH:MM:SS. detail_description should be alphanumeric only."
        }, 400, {"Content-Type": "application/json"}

    cursor = connection.cursor()
    try:
        cursor.execute(
            "DECLARE " +
            "USER_ID_IN VARCHAR2(36);" +
            "ACTION_START_IN DATE;" +
            "ACTION_STOP_IN DATE;" +
            "BOOK_ID_IN NUMBER;" +
            "DETAIL_DESCRIPTION_IN VARCHAR2(100);" +
            "ACTION_KEY_ID_IN NUMBER;" +
            "BEGIN " +
            "USER_ID_IN := '" + token["sub"]+"'; " +
            "ACTION_START_IN := TO_DATE('" + request.form["action_start"]+"', 'YYYY-MM-DD HH24:MI:SS'); " +
            "ACTION_STOP_IN := TO_DATE('" + request.form["action_stop"]+"',  'YYYY-MM-DD HH24:MI:SS'); " +
            "BOOK_ID_IN := " + request.form["book_id"]+"; " +
            "DETAIL_DESCRIPTION_IN := '" + request.form["detail_description"] + "'; " +
            "ACTION_KEY_ID_IN := " + request.form["action_key_id"] + "; " +
            "CHECK_DETAIL_ID_PROC (" +
            "USER_ID_IN => USER_ID_IN, " +
            "ACTION_START_IN => ACTION_START_IN, " +
            "ACTION_STOP_IN => ACTION_STOP_IN, " +
            "BOOK_ID_IN => BOOK_ID_IN, " +
            "DETAIL_DESCRIPTION_IN => DETAIL_DESCRIPTION_IN, " +
            "ACTION_KEY_ID_IN => ACTION_KEY_ID_IN " +
            ");" +
            "END;"
        )
        connection.commit()
    except cx_Oracle.Error as e:
        return{
            "status": "fail",
            "fail_no": 4,
            "message": "Error when updating database action",
            "database_message": str(e)
        }, 400, {"Content-Type": "application/json"}
    return {
        "status": "ok"
    }
