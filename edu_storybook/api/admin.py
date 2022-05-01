"""
admin.py

Routes beginning with `/api/admin/`.

Routes:

```
/api/admin/book/download
/api/admin/book/upload
/api/admin/book/study
/api/admin/book/grant
/api/admin/page
/api/admin/download/user
/api/admin/download/action
/api/admin/get/user
/api/admin/study/user
/api/admin/school
/api/admin/book/update
/api/admin/study
/api/admin/download/free_response
```
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
import logging
import random
import string
import datetime
import bcrypt
import time
import shutil

from edu_storybook.core.auth import validate_login, issue_auth_token
from edu_storybook.core.bucket import upload_bucket_file, download_bucket_file
from edu_storybook.core.helper import allowed_file, label_results_from, sanitize_redirects
from edu_storybook.core.email import send_email
from edu_storybook.core.config import Config, temp_folder
from edu_storybook.core.db import pool
from edu_storybook.core.sensitive import jwt_key
from edu_storybook.core.remove_watchdog import future_del_temp
from edu_storybook.core.reg_exps import *
from edu_storybook.core.helper import sanitize_redirects

a_admin = Blueprint('a_admin', __name__)

a_admin_log = logging.getLogger('api.admin')
if Config.production == False:
    a_admin_log.setLevel(logging.DEBUG)

@a_admin.route("/api/admin/book/download", methods=['POST'])
def admin_download_book():
    """
    Endpoint to allow the administrator download a book.

    Expects:
     - `filename`: The filename of the book.

    Fails:
     - `14`: Unable to download and/or send file.

    Returns: The file requested to be downloaded from the bucket.
    """
    # validate that user has admin rights to download books
    auth = request.cookies.get('Authorization')
    vl = validate_login(
        auth,
        permission=1
    )
    if vl != True:
        a_admin_log.debug(
            'Unauthenticated user tried to access admin_download_book'
        )
        return vl

    # check to make sure you have a 'filename'
    try:
        assert 'filename' in request.form
    except AssertionError:
        a_admin_log.debug(
            'The filename of the file to download was not provided by the admin'
        )
        return {
            "status": "fail",
            "fail_no": 1,
            "message": "filename was not provided."
        }, 400, {"Content-Type": "application/json"}

    # get file name from request
    fileInput = request.form['filename']
    try:
        # download file to bucket
        filepath = download_bucket_file(fileInput)
        # send file back
        return send_file(filepath)
    except:
        a_admin_log.warning(
            'Unable to download a file from the bucket, admin_download_book'
        )
        return {
            "status": "fail",
            "fail_no": 14,
            "message": "could not download file"
        }, 400, {"Content-Type": "application/json"}


@a_admin.route("/api/admin/book/upload", methods=['POST'])
def admin_book_upload():
    """
    Endpint to allow an administrator to upload a book.

    Expects:
     - `book_name`: The name of the book.
     - `book_description`: The description of the book.
     - `study_ids`: HTML checkbox list of selected study IDs to add the book to.

    Fails:
     - `10`: No file uploaded.
     - `11`: Filename was an empty string.
     - `12`: Error when uploading file to server data bucket.
     - `13`: Error when querying database.

    Returns: If everything worked, and no redirect was specified, then
    `{"status": "ok"}`. If everything worked, and a redirect was specified, then
    the user will be redirected. If there was a problem, then
    `{"status": "fail", ...}`.
    """
    # validate that user has admin rights to upload books
    auth = request.cookies.get('Authorization')
    vl = validate_login(
        auth,
        permission=1
    )
    if vl != True:
        a_admin_log.debug(
            'Unauthenticated user tried to access admin_book_upload'
        )
        return vl

    # check to make sure you have a 'book_name' and 'book_description
    try:
        assert 'book_name' in request.form
        assert 'book_description' in request.form
    except AssertionError:
        a_admin_log.debug(
            'An admin did not provided either book_name or book_description ' +\
                'when uploading a book'
        )
        return {
            "status": "fail",
            "fail_no": 1,
            "message": "book_name or book_description was not provided."
        }, 400, {"Content-Type": "application/json"}

    # get parameters for adding to book table
    book_name = (request.form.get('title')).strip() # Gives us the value of 'book name' field from frontend
    book_description = (request.form.get('description')).strip() # Gives us the value of 'book description' field from frontend
    study_ids = request.form.getlist('study_id') # Gives us the list of all study ids that are being selected on frontend

    # check if the post request has the file part
    if 'file' not in request.files:
        a_admin_log.debug('User did not provide a file in admin_book_upload')
        return {
            "status": "fail",
            "fail_no": 10,
            "message": "no file selected"
        }, 400, {"Content-Type": "application/json"}

    # get file from request files
    file = request.files['file']

    if file.filename == '':
        a_admin_log.debug(
            'User did not provide a filename for the file in admin_book_upload'
        )
        return {
            "status": "fail",
            "fail_no": 11,
            "message": "filename is empty string"
        }, 400, {"Content-Type": "application/json"}

    if file and allowed_file(file.filename):
        # prepend unique uuid for filename
        filename = str(uuid.uuid4()) + "_" + file.filename

        # save file to local /temp/file_upload folder
        file_path = os.path.join( temp_folder, filename )
        file.save(file_path)

        # convert pdf to images
        book_pngs = convert_from_path(file_path, 500)

        # remove .pdf extension from filename
        filename = filename.rstrip(".pdf")

        # make folder to store images
        upload_temp_folder = os.path.join(temp_folder, 'file_upload/')
        if not os.path.exists( upload_temp_folder ):
            os.makedirs( upload_temp_folder )

        # 1) insert files into bucket
        try:
            # iterate through length of book
            for i in range(len(book_pngs)):
                # Save pages as images in the pdf
                file_upload_folder = os.path.join(
                    upload_temp_folder,
                    filename
                )
                if not os.path.exists( file_upload_folder ):
                    os.makedirs( file_upload_folder )
                book_image_name = filename + '_' + str(i+1) + '.png'
                file_upload_image_path = os.path.join(
                    upload_temp_folder,
                    os.path.join(
                        filename,
                        book_image_name
                    )
                )
                book_pngs[i].save(file_upload_image_path, 'PNG')
                # upload images to a folder in bucket
                upload_bucket_file(file_upload_image_path, filename + '/' + book_image_name)
                # remove img file
                os.remove(file_upload_image_path)

            # remove temp dir
            shutil.rmtree( upload_temp_folder )

        except Exception as e:
            a_admin_log.warning('There was an error when trying to upload a ' +\
                'book to the bucket')
            a_admin_log.warning(e)
            return {
                "status": "fail",
                "fail_no": 12,
                "message": "Error when trying to upload file.",
                "flask_message": str(e)
            }, 400, {"Content-Type": "application/json"}

        # connect to database
        connection = pool.acquire()
        cursor = connection.cursor()

        # 2) insert book into 'book' table
        try:
            cursor.execute("INSERT into BOOK (book_name, description, folder, page_count) VALUES ('"
                           + book_name + "', '"
                           + book_description + "', '"
                           + filename + "', "
                           + str(len(book_pngs)) + ")")
            # commit to database
            connection.commit()
        except cx_Oracle.Error as e:
            a_admin_log.warning('Error when accessing the database')
            a_admin_log.warning(e)
            return {
                "status": "fail",
                "fail_no": 13,
                "message": "Error when querying database. 1159",
                "database_message": str(e)
            }

        # 3) Get book_id from 'book' table (given book name and its description) to insert entries in 'book_study' later
        try:
            cursor.execute("SELECT BOOK_ID FROM BOOK " +
                           "WHERE BOOK_NAME='" + book_name + "' AND DESCRIPTION='" + book_description + "'")
            label_results_from(cursor)
        except cx_Oracle.Error as e:
            a_admin_log.warning('Error when accessing the database')
            a_admin_log.warning(e)
            return {
                "status": "fail",
                "fail_no": 14,
                "message": "Error when querying database. 1160",
                "database_message": str(e)
            }

        book_id = cursor.fetchone()
        if book_id is None:
            a_admin_log.debug('Book ID not found from the parameter values ' +\
                'upon querying database')
            return {
                "status": "fail",
                "fail_no": 15,
                "message": "book id not found upon querying database"
            }, 400, {"Content-Type": "application/json"}

        # 4) insert studies assigned to a book in 'book_study' table
        try:
            # Iterate through all study ids and insert them one-by-one to a 'book_study' table
            for study_id in study_ids:
                cursor.execute("INSERT into BOOK_STUDY (book_id, study_id) VALUES ("
                               + request.form['BOOK_ID'] + ", "
                               + str(study_id) + ")")
            # commit to database
            connection.commit()
        except cx_Oracle.Error as e:
            a_admin_log.warning('Error when accessing the database')
            a_admin_log.warning(e)
            return {
                "status": "fail",
                "fail_no": 16,
                "message": "Error when querying database. 1161",
                "database_message": str(e)
            }

        res = None
        if 'redirect' in request.form:
            user_redirect_url = sanitize_redirects(request.form['redirect'])
            res = make_response(redirect(user_redirect_url))
        else:
            res = make_response({
                "status": "ok"
            })

        return res
    else:
        a_admin_log.debug(
            'User uploaded a file with an invalid extension in admin_book_upload'
        )
        return {
            "status": "fail",
            "fail_no": 17,
            "message": "invalid file format or file"
        }, 400, {"Content-Type": "application/json"}


@a_admin.route("/api/admin/book/study", methods=['POST'])
def admin_book_study():
    # validate that user has admin rights to upload books
    auth = request.cookies.get('Authorization')
    vl = validate_login(
        auth,
        permission=1
    )
    if vl != True:
        a_admin_log.debug(
            'Unauthenticated user tried to access admin_book_upload'
        )
        return vl
    try:
        assert "direction" in request.form
    except AssertionError:
        a_admin_log.debug(
            'An admin did not provide a book_id ' +\
                'when creating book_study relation'
        )
        return {
            "status": "fail",
            "fail_no": 1,
            "message": "book_id was not provided."
        }, 400, {"Content-Type": "application/json"}

    if request.form['direction'] == 'stob':

        # check to make sure you have a 'book_id'
        try:
            assert 'book_id' in request.form
        except AssertionError:
            a_admin_log.debug(
                'An admin did not provide a book_id ' +\
                    'when creating book_study relation'
            )
            return {
                "status": "fail",
                "fail_no": 1,
                "message": "book_id was not provided."
            }, 400, {"Content-Type": "application/json"}

        study_ids = request.form.getlist('study_id') # Gives us the list of all study ids that are being selected on frontend
        cursor = connection.cursor()

        try:
            conn_lock.acquire()
            # Iterate through all study ids and insert them one-by-one to a 'book_study' table
            for study_id in study_ids:
                cursor.execute("INSERT into BOOK_STUDY (book_id, study_id) VALUES ("
                    + request.form['book_id'] + ", "
                    + str(study_id) + ")")
                # commit to database
                connection.commit()
        except cx_Oracle.Error as e:
            a_admin_log.warning('Error when accessing the database')
            a_admin_log.warning(e)
            return {
                "status": "fail",
                "fail_no": 16,
                "message": "Error when querying database. 1161",
                "database_message": str(e)
            }
        finally:
            conn_lock.release()
    elif request.form['direction'] =='btos':
        # check to make sure you have a 'book_id'
        try:
            assert 'study_id' in request.form
        except AssertionError:
            a_admin_log.debug(
                'An admin did not provide a book_id ' +\
                    'when creating book_study relation'
            )
            return {
                "status": "fail",
                "fail_no": 1,
                "message": "book_id was not provided."
            }, 400, {"Content-Type": "application/json"}

        book_ids = request.form.getlist('book_id') # Gives us the list of all study ids that are being selected on frontend
        cursor = connection.cursor()

        try:
            conn_lock.acquire()
            # Iterate through all study ids and insert them one-by-one to a 'book_study' table
            for book_id in book_ids:
                cursor.execute('INSERT into BOOK_STUDY (book_id, study_id) VALUES ('
                    + str(book_id)+ ', '
                    + request.form['study_id'] +')')
                # commit to database
                connection.commit()

        except cx_Oracle.Error as e:
            a_admin_log.warning('Error when accessing the database')
            a_admin_log.warning(e)
            return {
                "status": "fail",
                "fail_no": 67,
                "message": "Error when querying database. 1161",
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
    return res


@a_admin.route("/api/admin/book/grant", methods=['POST'])
def admin_add_book_to_study():
    '''
    Add a book to a study.
    '''
    # validate that user can access data
    auth = request.cookies.get('Authorization')
    vl = validate_login(
        auth,
        permission=1
    )
    if vl != True:
        return vl

    # check input params
    try:
        assert 'book_name' in request.form
        assert 'book_url' in request.form
        assert 'book_description' in request.form
        assert 'study_id' in request.form
    except AssertionError:
        a_admin_log.debug(
            'An admin did not provided one or more fields when adding a book' +\
                'to a study'
        )
        return {
            "status": "fail",
            "fail_no": 1,
            "message": "book_name, book_url, book_description, and/or study_id was not provided."
        }, 400, {"Content-Type": "application/json"}

    # get parameters
    book_name = (request.form.get('book_name')).lower().strip()
    book_url = (request.form.get('book_url')).lower().strip()
    book_description = (request.form.get('book_description')).lower().strip()
    study_id = (request.form.get('study_id'))
    # book_id and created_on handled by trigger

    # connect to database
    connection = pool.acquire()
    cursor = connection.cursor()

    # insert query
    try:
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
        a_admin_log.warning('Error when accessing database')
        a_admin_log.warning(e)
        return {
            "status": "fail",
            "fail_no": 4,
            "message": "Error when querying database.",
            "database_message": str(e)
        }


@a_admin.route("/api/admin/page", methods=['POST', 'GET', 'PUT', 'DELETE'])
def admin_page_handler():
    """
    This endpoint handles quiz questions and answers. This allows an admin to
    create, get, update, or delete quiz questions and their answers.
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
    token = jwt.decode(auth, jwt_key, algorithms=Config.jwt_alg)

    # grab a connection
    connection = pool.acquire()

    if request.method == 'POST':
        # check to make sure you have a book_id
        try:
            assert 'book_id_in' in request.form
            assert 'question_in' in request.form
            assert 'page_prev_in' in request.form
            assert 'page_next_in' in request.form
            assert 'answers_in' in request.form
            assert 'question_type_in' in request.form
            assert 'answers_feedback_in' in request.form
            assert 'answers_correct_in' in request.form
        except AssertionError:
            a_admin_log.debug('An admin did not provide all of the form ' +\
                'fields when creating a question')
            return {
                "status": "fail",
                "fail_no": 1,
                "message": "book_id_in, question_in, page_prev_in, page_next_in, answers_in, question_type_in, answers_feedback_in, answers_correct_in not provided"
            }, 400, {"Content-Type": "application/json"}

        # sanitize inputs: check ints
        try:
            book_id_in = int(request.form['book_id_in'])
            page_prev_in = int(request.form['page_prev_in'])
            page_next_in = int(request.form['page_next_in'])
            question_type_in = int(request.form['question_type_in'])
        except ValueError:
            a_admin_log.debug('An admin provided non-int form data when ' +\
                'creating a question')
            return {
                "status": "fail",
                "fail_no": 2,
                "message": "book_id_in, page_prev_in, page_next_in, or question_type_in failed a sanitize check. The posted fields should be integers."
            }, 400, {"Content-Type": "application/json"}

        # not sanitizing questions or answers. may have any text since its up to the customer's discretion what the question is
        # regex is not very efficient method here for sql injection check
        cursor = connection.cursor()

        print(request.form['answers_feedback_in'])
        try:
            cursor.callproc("insert_question_proc",\
                [request.form['question_in'],\
                    request.form['book_id_in'],\
                    request.form['page_prev_in'],\
                    request.form['page_next_in'],\
                    request.form['answers_in'],\
                    request.form['question_type_in'],\
                    request.form['answers_feedback_in'],\
                    request.form['answers_correct_in']])
            # commit changes to db
            connection.commit()
        except cx_Oracle.Error as e:
            a_admin_log.warning('Error when accessing the database')
            a_admin_log.warning(e)
            return {
                "status": "fail",
                "fail_no": 3,
                "message": "Error when querying database. line 889",
                "database_message": str(e)
            }, 400, {"Content-Type": "application/json"}

        return {
          "status": "ok"
        }

    elif request.method == 'GET':  # Get = get (retrieve pages)
        cursor = connection.cursor()

        # check to make sure you have a book_id
        try:
            assert 'book_id' in request.form
        except AssertionError:
            a_admin_log.debug('An admin did not provide the book_id of ' +\
                'the book when getting a question')
            return {
                "status": "fail",
                "fail_no": 1,
                "message": "book_id was not provided."
            }, 400, {"Content-Type": "application/json"}

        try:
            book_id = int(request.form['book_id'])
        except ValueError:
            a_admin_log.debug('An admin provided non-int form data when ' +\
                'getting a question')
            return {
                "status": "fail",
                "fail_no": 2,
                "message": "book_id failed a sanitize check. The POSTed field should be an integer."
            }, 400, {"Content-Type": "application/json"}

        try:
            cursor.execute(
                "SELECT QUESTION.QUESTION_ID, QUESTION.QUESTION, ANSWER.ANSWER FROM QUESTION " +
                "INNER JOIN USER_RESPONSE ON USER_RESPONSE.QUESTION_ID = QUESTION.QUESTION_ID " +
                "INNER JOIN ANSWER ON USER_RESPONSE.QUESTION_ID = ANSWER.QUESTION_ID " +
                "WHERE BOOK_ID=" + request.form["book_id"]
            )
            label_results_from(cursor)
        except cx_Oracle.Error as e:
            a_admin_log.warning('Error when accessing the database')
            a_admin_log.warning(e)
            return {
                "status": "fail",
                "fail_no": 3,
                "message": "Error when querying database.",
                "database_message": str(e)
            }, 400, {"Content-Type": "application/json"}

        # fetching all the questions and storing them in questions array
        questions = []

        while True:
            result = cursor.fetchone()
            if result is None:
                break
            questions.append(result)
        if len(questions) == 0:
            a_admin_log.debug('An admin provided an invalid book_id when ' +\
                'getting the questions for a book.')
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
            a_admin_log.debug('An admin did not provide all of the form ' +\
                'fields when updating a question')
            return {
                "status": "fail",
                "fail_no": 1,
                "message": "question_id_in, question_in, or answers_in not provided"
            }, 400, {"Content-Type": "application/json"}

        # check that question id is an int
        try:
            question_id = int(request.form['question_id_in'])
        except ValueError:
            a_admin_log.debug('An admin provided non-int form data when ' +\
                'getting a question')
            return {
                "status": "fail",
                "fail_no": 2,
                "message": "question_id failed a sanitize check. The POSTed field should be an integer."
            }, 400, {"Content-Type": "application/json"}

        # try query calling procedure "edit_question_proc"
        cursor = connection.cursor()
        try:
            cursor.callproc("edit_question_proc",\
                [request.form['question_id_in'],\
                    request.form['question_in'],\
                    request.form['answers_in']])
            # commit changes to db
            connection.commit()
        except cx_Oracle.Error as e:
            a_admin_log.warning('Error when accessing the database')
            a_admin_log.warning(e)
            return {
                "status": "fail",
                "fail_no": 3,
                "message": "Error when querying database. line 889",
                "database_message": str(e)
            }, 400, {"Content-Type": "application/json"}

        return {
          "status": "ok"
        }

    elif request.method == 'DELETE':  # DELETE = delete a page
        # check correct inputs
        try:
            assert 'question_id_in' in request.form
        except AssertionError:
            a_admin_log.debug('An admin did not provide all of the form ' +\
                'fields (question_id_in) when deleting a question.')
            return {
                "status": "fail",
                "fail_no": 1,
                "message": "question_id_in was not provided"
            }, 400, {"Content-Type": "application/json"}

        try:
            question_id_in = int(request.form['question_id_in'])
        except ValueError:
            a_admin_log.debug('An admin did not provide all of the form ' +\
                'fields when deleting a question')
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
            a_admin_log.warning('Error when accessing database')
            a_admin_log.warning(e)
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
        a_admin_log.warning(
            'This error should not even be possible in admin_page_handler, as' +
            'it would require the user using an HTTP method that is not GET, ' +
            'POST, PUT, or DELETE, but somehow allowed by Flask; even though ' +
            'this endpoint specifically only allows those HTTP methods.'
        )
        return {
            "status": "fail",
            "fail_no": 5,
            "message": "Invalid HTTP operation, not GET, POST, PUT, or DELETE"
        }, 400, {"Content-Type": "application/json"}


@a_admin.route("/api/admin/download/user", methods=['GET'])
def admin_download_user_data():
    """
    Exports user profile data to a csv file.

    - Connects to database.
    - Computes a select query to get user profile data.
    - calls create_csv(query_results, headers) to create csv-formatted string.
    - creates and returns csv file using csv-formatted string.
    """
    # validate that user can access data
    auth = request.cookies.get('Authorization')
    vl = validate_login(
        auth,
        permission=1
    )
    if vl != True:
        return vl

    # connect to database
    connection = pool.acquire()
    cursor = connection.cursor()

    # select query
    try:
        cursor.execute("SELECT USER_PROFILE.EMAIL, USER_PROFILE.USER_ID, USER_PROFILE.FIRST_NAME, USER_PROFILE.LAST_NAME, USER_PROFILE.CREATED_ON, USER_PROFILE.LAST_LOGIN, SCHOOL.SCHOOL_NAME, LISTAGG(STUDY.STUDY_NAME, ';') WITHIN GROUP(ORDER BY STUDY.STUDY_NAME) AS STUDIES "
                       "FROM USER_PROFILE "
                       "INNER JOIN SCHOOL ON USER_PROFILE.SCHOOL_ID = SCHOOL.SCHOOL_ID "
                       "INNER JOIN USER_STUDY ON USER_PROFILE.USER_ID = USER_STUDY.USER_ID "
                       "INNER JOIN STUDY ON USER_STUDY.STUDY_ID = STUDY.STUDY_ID "
                       "GROUP BY USER_PROFILE.EMAIL, USER_PROFILE.USER_ID, USER_PROFILE.FIRST_NAME, USER_PROFILE.LAST_NAME, USER_PROFILE.CREATED_ON, USER_PROFILE.LAST_LOGIN, SCHOOL.SCHOOL_NAME")
    except cx_Oracle.Error as e:
        a_admin_log.warning('Error when accessing database')
        a_admin_log.warning(e)
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
        "User ID",
        "Email",
        "First Name",
        "Last Name",
        "Created On",
        "Last Login",
        "School",
        "Studies"
    ]

    # create filename with unique guid to prevent duplicates
    filename = "temp/csv_export_" + str(uuid.uuid4()) + ".csv"

    # write data to new csv file in data/csv_exports
    with open(filename, 'w', newline="") as csvfile:
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
            data = f.read(Config.buffer_size)
            if not data:
                break
            sha1.update(data)

    # queue the file to be removed
    future_del_temp(filename)

    try: # return response
        return send_file(filename, mimetype="text/csv", attachment_filename="user.csv", as_attachment=True, etag=sha1.hexdigest())
    except Exception as e:
        a_admin_log.warning('Was unable to CSV data file back to user')
        a_admin_log.warning(e)
        return {
            "status": "fail",
            "fail_no": 9,
            "message": "Error when sending csv file.",
            "flask_message": str(e)
        }


@a_admin.route("/api/admin/download/action", methods=['GET'])
def admin_download_action_data():
    """
    Exports user action data to a csv file.

    - Connects to database.
    - Calls a procedure to get user profile data.
    - calls create_csv(query_results, headers) to create csv-formatted string.
    - creates and returns csv file using csv-formatted string.
    """
    # validate that user can access data
    auth = request.cookies.get('Authorization')
    vl = validate_login(
        auth,
        permission=1
    )
    if vl != True:
        return vl

    # connect to database
    connection = pool.acquire()
    cursor = connection.cursor()

    # select query
    try:
        result = cursor.var(cx_Oracle.CURSOR)
        cursor.callproc("GET_USER_PROFILE_DATA_PROC", \
            [result])
        
    except cx_Oracle.Error as e:
        a_admin_log.warning('Error when accessing database')
        a_admin_log.warning(e)
        return {
            "status": "fail",
            "fail_no": 4,
            "message": "Error when querying database.",
            "database_message": str(e)
        }

    # assign variable data to cursor.fetchall(). if i do not assign it to a variable, Response() sees it as an empty string
    data = result.getvalue().fetchall()

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
    filename = temp_folder + "csv_export_" + str(uuid.uuid4()) + ".csv"

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
            data = f.read(Config.buffer_size)
            if not data:
                break
            sha1.update(data)

    # queue the file to be removed
    future_del_temp(filename)

    try: # return response
        return send_file(filename, mimetype="text/csv", attachment_filename="action.csv", as_attachment=True, etag=sha1.hexdigest())
    except Exception as e:
        a_admin_log.warning('Error when sending CSV data file to user')
        a_admin_log.warning(e)
        return {
            "status": "fail",
            "fail_no": 9,
            "message": "Error when sending csv file.",
            "flask_message": str(e)
        }


# take in input param ofset that will be the limit of 50 ofset of 50 and then be happy.
@a_admin.route("/api/admin/get/user/<int:offset>", methods=['GET'])
def admin_get_users(offset:int):
    """
    Exports user data to a JSON.

    - Connects to database.
    - Computes a select query to get user data.
    - return USER_ID, USERNAME (full), STUDY that they currently belong to.
        Important: Sort by join date, or login date, or something. We want fresh
        users first.
    - Allow an admin to retrieve a JSON list of all of the users.
        LIMIT the response to only 50 rows, and use the PL/SQL OFFSET to offset
        to grab the first 50 rows, then next 50 rows.
        Make offset an input parameter (int).
    """

    # validate that user has rights to access
    auth = request.cookies.get('Authorization')
    vl = validate_login(
        auth,
        permission=1
    )
    if vl != True:
        return vl

    if 'Bearer ' in auth:
        auth = auth.replace('Bearer ', '', 1)

    token = jwt.decode(auth, jwt_key, algorithms=Config.jwt_alg)

    # connect to database
    connection = pool.acquire()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT USER_ID, FIRST_NAME, LAST_NAME, EMAIL FROM USER_PROFILE ORDER BY CREATED_ON DESC OFFSET " +
            str(offset) + " ROWS FETCH NEXT 50 ROWS ONLY"
        )
        label_results_from(cursor)
    except cx_Oracle.Error as e:
        a_admin_log.warning('Error when accessing database')
        a_admin_log.warning(e)
        return {
            "status": "fail",
            "fail_no": 3,
            "message": "Error when accessing database.",
            "database_message": str(e)
        }, 400, {"Content-Type": "application/json"}

    users = cursor.fetchall()
    return {
        "users": users
    }

@a_admin.route("/api/admin/get/book/<int:offset>", methods=['GET'])
def admin_get_books(offset: int):
    """
    Exports book data to a JSON.

    - Connects to database
    - Computes a select query to get book data
    - Return BOOK_ID, BOOKNAME , DESCRIPTION, PAGE_COUNT
    - Allow an admin to retrieve a JSON list of all of the users.
        LIMIT the response to only 50 rows, and use the PL/SQL OFFSET to offset
        to grab the first 50 rows, then next 50 rows.
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

    token = jwt.decode(auth, jwt_key, algorithms=Config.jwt_alg)

    # connect to database
    connection = pool.acquire()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT BOOK.BOOK_ID, BOOK.BOOK_NAME, BOOK.DESCRIPTION, BOOK_STUDY.STUDY_ID FROM BOOK " +
            "INNER JOIN BOOK_STUDY ON BOOK_STUDY.BOOK_ID = BOOK.BOOK_ID "+
            "OFFSET "+
            str(offset) +" ROWS FETCH NEXT 50 ROWS ONLY"
        )
        label_results_from(cursor)
    except cx_Oracle.Error as e:
        a_admin_log.warning('Error when accessing database')
        a_admin_log.warning(e)
        return {
            "status": "fail",
            "fail_no": 3,
            "message": "Error when accessing database.",
            "database_message": str(e)
        }, 400, {"Content-Type": "application/json"}

    books = cursor.fetchall()

    return {
        "books": books
    }


@a_admin.route("/api/admin/study/user", methods=['GET', 'POST', 'DELETE'])
def admin_study_user():
    '''
    'POST' and 'DELETE' methods for admin adding and removing users from studies
    'GET" method for admin to get users associated with a specific study
    '''
     # validate that user has rights
    auth = request.cookies.get('Authorization')
    vl = validate_login(
        auth,
        permission=1
    )
    if vl != True:
        return vl

    if 'Bearer ' in auth:
        auth = auth.replace('Bearer ', '', 1)

    token = jwt.decode(auth, jwt_key, algorithms=Config.jwt_alg)

    if request.method == "GET":
        cursor = connection.cursor()

        try:
            study_id = int(request.args.get('study_id'))
        except ValueError:
            return {
                "status": "fail",
                "fail_no": 2,
                "message": "study_id failed a sanitize check. The POSTed field should be an integer."
            }, 400, {"Content-Type": "application/json"}

        try:
            cursor.execute("SELECT * from user_study "
                    +  "full outer join user_profile on user_study.user_id = user_profile.user_id "
                    + "where user_study.study_id = "+ str(study_id))
            label_results_from(cursor)
            users = cursor.fetchall()


            return{
                "users": users
            }
        except cx_Oracle.Error as e:
            return {
                "status": "fail",
                "fail_no": 3,
                "message": "Error when accessing database.",
                "database_message": str(e)
            }, 400, {"Content-Type": "application/json"}

    #check for study_id and user_id

    try:
        #assert 'study_id' in request.form
        assert 'user_id' in request.form
    except AssertionError:
        return {
            "status": "fail",
            "fail_no": 1,
            "message": "user_id was not provided."
        }, 400, {"Content-Type": "application/json"}

    # do the right method
    if request.method =='POST':
        study_ids = request.form.getlist('study_id') # Gives us the list of all study ids that are being selected on frontend

        cursor = connection.cursor()

        try:
            for study_id in study_ids:
                cursor.execute(
               "INSERT INTO user_study(user_id, study_id) VALUES('"
                   + request.form['user_id']+ "', " +str(study_id)+")")

            # commit changes to db
            connection.commit()
        except cx_Oracle.Error as e:
            return {
                "status": "fail",
                "fail_no": 3,
                "message": "Error when accessing database.",
                "database_message": str(e)
            }, 400, {"Content-Type": "application/json"}


    elif request.method == 'DELETE':
        cursor = connection.cursor()

        try:
            cursor.callproc("delete_user_study_proc",\
                [request.form['user_id'], int(request.form['study_id'])])

            connection.commit()
        except cx_Oracle.Error as e:
            return {
                "status": "fail",
                "fail_no": 4,
                "message": "Error when accessing database.",
                "database_message": str(e)
            }, 400, {"Content-Type": "application/json"}

    res = None
    if 'redirect' in request.form:
        user_redirect_url = sanitize_redirects(request.form['redirect'])
        res = make_response(redirect(user_redirect_url))
    else:
        res = make_response({
            "status": "ok"
        })
    return res


@a_admin.route("/api/admin/school", methods=['GET', 'POST', 'PUT', 'DELETE'])
def admin_school():
    '''
    'GET', 'POST', 'PUT', and 'DELETE' methods to get the full list of schools, create a new school, update a school, or delete a school.
    '''
     # validate that user has rights
    auth = request.cookies.get('Authorization')
    vl = validate_login(
        auth,
        permission=1
    )
    if vl != True:
        return vl

    if 'Bearer ' in auth:
        auth = auth.replace('Bearer ', '', 1)

    token = jwt.decode(auth, jwt_key, algorithms=Config.jwt_alg)

    # grab db connection
    connection = pool.acquire()

    # return the full list of schools
    if request.method =='GET':
        cursor = connection.cursor()

        try:
            cursor.execute(
                "SELECT SCHOOL_NAME FROM SCHOOL ORDER BY SCHOOL_ID"
            )
            label_results_from(cursor)

        except cx_Oracle.Error as e:
            a_admin_log.warning('Error when accessing database')
            a_admin_log.warning(e)
            return {
                "status": "fail",
                "fail_no": 3,
                "message": "Error when accessing database.",
                "database_message": str(e)
            }, 400, {"Content-Type": "application/json"}

        schools = cursor.fetchall()

        return {
            "schools": schools
        }

    # check for school_id and school_name
    try:
        assert 'school_name' in request.form
    except AssertionError:
        a_admin_log.debug('An admin did not provide the school_name or school_id when ' +\
            'updating  data for a book')
        return {
            "status": "fail",
            "fail_no": 1,
            "message": "school_id or school_name was not provided."
        }, 400, {"Content-Type": "application/json"}


    # check if post method
    if request.method == 'POST':
        cursor = connection.cursor()

        try:
            cursor.callproc("insert_school_proc",\
                [request.form['school_name']])
            connection.commit()
        except cx_Oracle.Error as e:
            a_admin_log.warning('Error when accessing database')
            a_admin_log.warning(e)
            return {
                "status": "fail",
                "fail_no": 4,
                "message": "Error when accessing database.",
                "database_message": str(e)
            }, 400, {"Content-Type": "application/json"}
        return{
            "status":"ok"
        }
    try:
        assert 'school_id' in request.form
    except AssertionError:
        a_admin_log.debug('An admin did not provide the school_name or school_id when ' +\
            'updating  data for a book')
        return {
            "status": "fail",
            "fail_no": 1,
            "message": "school_id or school_name was not provided."
        }, 400, {"Content-Type": "application/json"}


    #make sure school_id is an int
    try:
        school_id = int(request.form['school_id'])
    except ValueError:
        a_admin_log.debug('An admin did not provide a numerical school_id when ' +\
            'updating  data for a book')
        return {
            "status": "fail",
            "fail_no": 2,
            "message": "school_id failed a sanitize check. The POSTed field should be an integer."
        }, 400, {"Content-Type": "application/json"}
    # check if put method
    if request.method == 'PUT':
        cursor = connection.cursor()

        try:
            cursor.callproc("edit_school_proc",\
                [int(request.form['school_id']), request.form['school_name']])
            connection.commit()
        except cx_Oracle.Error as e:
            a_admin_log.warning('Error when accessing database')
            a_admin_log.warning(e)
            return {
                "status": "fail",
                "fail_no": 4,
                "message": "Error when accessing database.",
                "database_message": str(e)
            }, 400, {"Content-Type": "application/json"}

    # TODO: Fix cascading delete with schools that reference delete
    # check if school name and id and then delete it
    '''
    elif request.method == 'DELETE':
        cursor = connection.cursor()

        try:
            cursor.callproc("delete_school_proc",\
                [int(request.form['school_id']), request.form['school_name']])
        except cx_Oracle.Error as e:
            a_admin_log.warning('Error when accessing database')
            a_admin_log.warning(e)
            return {
                "status": "fail",
                "fail_no": 4,
                "message": "Error when accessing database.",
                "database_message": str(e)
            }, 400, {"Content-Type": "application/json"}
    '''

    return{
        'status':  'ok'
    }


@a_admin.route("/api/admin/book/update", methods=['POST'])
def admin_update_books():
    """
    Updates the name and description of a book.
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

    token = jwt.decode(auth, jwt_key, algorithms=Config.jwt_alg)

    # check to make sure you have a book name and book_description
    try:
        assert 'book_name' in request.form
        assert 'book_description' in request.form
        assert 'book_id' in request.form
    except AssertionError:
        a_admin_log.debug('An admin did not provide the book_name or description when ' +\
            'updating  data for a book')
        return {
            "status": "fail",
            "fail_no": 1,
            "message": "book_name or book_description was not provided."
        }, 400, {"Content-Type": "application/json"}

    try:
        book_id = int(request.form['book_id'])
    except ValueError:
        a_admin_log.debug('An admin did not provide a numerical book_id when ' +\
            'updating  data for a book')
        return {
            "status": "fail",
            "fail_no": 2,
            "message": "school_id failed a sanitize check. The POSTed field should be an integer."
        }, 400, {"Content-Type": "application/json"}

    # connect to database
    connection = pool.acquire()
    cursor = connection.cursor()

    try:
        cursor.callproc("edit_book_proc",\
            [int(request.form['book_id']), request.form['book_name'], request.form['book_description']])
        connection.commit()
    except cx_Oracle.Error as e:
        a_admin_log.warning('Error when accessing database')
        a_admin_log.warning(e)
        return {
            "status": "fail",
            "fail_no": 3,
            "message": "Error when accessing database.",
            "database_message": str(e)
        }, 400, {"Content-Type": "application/json"}

    return {
        "status": "ok"
    }



@a_admin.route("/api/admin/study", methods=['POST'])
def admin_create_study():
    """
    Allows admin to create a new study
    Take in study_id, school_id, study_name, and study_invite_code
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

    # check to make sure you have a book name and book_description 
    try:
        assert 'study_id' in request.form
        assert 'school_id' in request.form
        assert 'study_name' in request.form
        assert 'study_invite_code' in request.form
    except AssertionError:
        a_admin_log.debug('An admin did not provide one or more of the following (study_id, school_id, study_name, study_invite_code) when ' +\
            'adding a new study')
        return {
            "status": "fail",
            "fail_no": 1,
            "message": "book_name or book_description was not provided."
        }, 400, {"Content-Type": "application/json"}

    try:
        book_id = int(request.form['study_id'])
        school_id = int(request.form['school_id'])
        study_invite_code = int(request.form['study_invite_code'])
    except ValueError:
        a_admin_log.debug('An admin did not provide a numerical when ' +\
            'adding a new study')
        return {
            "status": "fail",
            "fail_no": 2,
            "message": "school_id failed a sanitize check. The POSTed field should be an integer."
        }, 400, {"Content-Type": "application/json"}

    # connect to database
    cursor = connection.cursor()

    try:
        cursor.execute("INSERT INTO STUDY (study_id, school_id, study_name, study_invite_code) VALUES("
            + request.form['study_id'] + "', '"
            + request.form['school_id'] + "', '"
            + request.form['study_name'] + "', "
            + request.form['study_invite_code'] + ")")
        connection.commit()
    except cx_Oracle.Error as e:
        a_admin_log.warning('Error when accessing database')
        a_admin_log.warning(e)
        return {
            "status": "fail",
            "fail_no": 3,
            "message": "Error when accessing database.",
            "database_message": str(e)
        }, 400, {"Content-Type": "application/json"}

    return {
        "status": "ok"
    }


@a_admin.route("/api/admin/download/free_response", methods=['GET'])
def admin_download_free_response():
    """
    Exports user free response data to a csv file.

    - Connects to database.
    - Calls a procedure to get user free response data.
    - calls create_csv(query_results, headers) to create csv-formatted string.
    - creates and returns csv file using csv-formatted string.
    """
    # validate that user can access data
    auth = request.cookies.get('Authorization')
    vl = validate_login(
        auth,
        permission=1
    )
    if vl != True:
        return vl

    # connect to database
    connection = pool.acquire()
    cursor = connection.cursor()

    # select query
    try:
        result = cursor.var(cx_Oracle.CURSOR)
        cursor.callproc("GET_USER_FREE_RESPONSE_DATA_PROC", \
            [result])
        
    except cx_Oracle.Error as e:
        a_admin_log.warning('Error when accessing database')
        a_admin_log.warning(e)
        return {
            "status": "fail",
            "fail_no": 4,
            "message": "Error when querying database.",
            "database_message": str(e)
        }

    # assign variable data to cursor.fetchall(). if i do not assign it to a variable, Response() sees it as an empty string
    data = result.getvalue().fetchall()

    # column headers for csv
    headers = [
        "Email",
        "First Name",
        "Last Name",
        "Question",
        "Response",
        "Book Name",
        "Submitted On"
    ]

    # create filename with unique guid to prevent duplicates
    filename = temp_folder + "csv_export_" + str(uuid.uuid4()) + ".csv"

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
            data = f.read(Config.buffer_size)
            if not data:
                break
            sha1.update(data)

    # queue the file to be removed
    future_del_temp(filename)

    try: # return response
        return send_file(filename, mimetype="text/csv", attachment_filename="free_response.csv", as_attachment=True, etag=sha1.hexdigest())
    except Exception as e:
        a_admin_log.warning('Error when sending CSV data file to user')
        a_admin_log.warning(e)
        return {
            "status": "fail",
            "fail_no": 9,
            "message": "Error when sending csv file.",
            "flask_message": str(e)
        }
