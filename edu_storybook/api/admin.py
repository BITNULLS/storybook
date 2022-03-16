"""
admin.py
    Routes beginning with /api/admin/

Routes:
    /api/admin/book/download
    /api/admin/book/upload
    /api/admin/book/grant
    /api/admin/page
    /api/admin/download/user
    /api/admin/download/action
    /api/admin/get/user
"""

from pydoc import Helper
from flask import request
from flask import make_response
from flask import Blueprint
from flask import send_file
from flask import redirect

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
import time

from core.auth import validate_login, issue_auth_token
from core.bucket import bucket
from core.helper import allowed_file, label_results_from, sanitize_redirects
from core.email import send_email
from core.config import config
from core.db import connection, conn_lock
from core.sensitive import jwt_key
from core.remove_watchdog import future_del_temp
from core.reg_exps import *
from core.helper import sanitize_redirects

a_admin = Blueprint('a_admin', __name__)

@a_admin.route("/api/admin/book/download", methods=['POST'])
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


@a_admin.route("/api/admin/book/upload", methods=['POST'])
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
    book_name = (request.form.get('title')).strip()
    book_description = (request.form.get('description')).strip()
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
        if not os.path.isdir('temp'):
            os.mkdir('temp')
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
        os.makedirs("temp/file_upload/" + filename)

        # 1) insert files into bucket
        try:
            # iterate through length of book
            for i in range(len(book_pngs)):
                # Save pages as images in the pdf
                book_pngs[i].save('temp/file_upload/' + filename +
                                  "/" + filename + "_" + str(i+1) + '.png', 'PNG')
                # upload images to a folder in bucket
                bucket.upload_bucket_file('temp/file_upload/' + filename + "/" + filename + "_" + str(
                    i+1) + '.png', filename + "/" + filename + "_" + str(i+1) + '.png')
                # remove img file
                os.remove('temp/file_upload/' + filename + "/" +
                          filename + "_" + str(i+1) + '.png')

            # remove temp dir
            os.rmdir("temp/file_upload/" + filename)

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

        res = None
        if 'redirect' in request.form:
            user_redirect_url = sanitize_redirects(request.form['redirect'])
            res = make_response(redirect(user_redirect_url))
        else:
            res = make_response({
                "status": "ok"
            })

    return {
        "status": "fail",
        "fail_no": 13,
        "message": "invalid file format or file"
    }, 400, {"Content-Type": "application/json"}

@a_admin.route("/api/admin/book/grant", methods=['POST'])
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


@a_admin.route("/api/admin/page", methods=['POST', 'GET', 'PUT', 'DELETE'])
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


@a_admin.route("/api/admin/download/user", methods=['POST'])
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


@a_admin.route("/api/admin/download/action", methods=['POST'])
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
@a_admin.route("/api/admin/get/user", methods=['GET'])
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
