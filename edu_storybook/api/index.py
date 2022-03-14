"""
index.py
    Handles all top level routes of the API.

Routes:
    /api/
    /api/book
    /api/schools
    /api/login
    /api/logout
    /api/register
"""

from flask import request
from flask import redirect
from flask import make_response
from flask import Blueprint

import uuid
import jwt
import cx_Oracle
import bcrypt
import time

from core.auth import validate_login, issue_auth_token
from core.bucket import bucket
from core.helper import allowed_file, label_results_from
from core.email import send_email
from core.config import config
from core.db import connection, conn_lock
from core.sensitive import jwt_key
from core.remove_watchdog import future_del_temp
from core.reg_exps import *

a_index = Blueprint('a_index', __name__)

@a_index.route("/api/")
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


@a_index.route("/api/book", methods=['GET'])
def get_users_books():
    # validate that user has rights to access books
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

    # connect to database
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT b.BOOK_ID FROM BOOK b "
            + "INNER JOIN STUDY s ON s.STUDY_ID = b.STUDY_ID "
            + "INNER JOIN USER_PROFILE u ON s.STUDY_ID = u.STUDY_ID "
            + "WHERE u.user_id='"
            + token['sub'] + "'"
        )
        label_results_from(cursor)
    except cx_Oracle.Error as e:
        return {
            "status": "fail",
            "fail_no": 4,
            "message": "Error when accessing books.",
            "database_message": str(e)
        }

    # assign variable data to cursor.fetchall()
    data = cursor.fetchall()

    print(data)

    return {
        "status": "ok"
    }


@a_index.route("/api/schools", methods=['GET'])
def get_schools():
    '''
    Return a list of schools in the same style/format/convention that 
    admin_get_users() returns a list of users.
    '''

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
            "SELECT SCHOOL_NAME FROM SCHOOL ORDER BY SCHOOL_ID OFFSET " +
            request.form["offset"] + " ROWS FETCH NEXT 50 ROWS ONLY"
        )
    except cx_Oracle.Error as e:
        return {
            "status": "fail",
            "fail_no": 3,
            "message": "Error when accessing database.",
            "database_message": str(e)
        }, 400, {"Content-Type": "application/json"}

    schools = cursor.fetchall()

    return {
        "schools": list(map(lambda x: x[0], schools))
    }


@a_index.route("/api/login", methods=['POST'])
def login():
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

    res = None
    if 'redirect' in request.form:
        res = make_response(redirect(request.form['redirect']))
    else:
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

@a_index.route("/api/logout")
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

@a_index.route("/api/register")
def register():
    # check that all expected inputs are not empty
    try:
        assert 'email' in request.form
        assert 'password' in request.form
        assert 'first_name' in request.form
        assert 'last_name' in request.form
        assert 'school_id' in request.form
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
