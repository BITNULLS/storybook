"""
auth.py
    ...

Functions:
    login()
    logout()
    register()
"""

import jwt
import time
import bcrypt
import uuid
import cx_Oracle
from flask import make_response

from core.sensitive import jwt_key
from config import config
from db import connection, conn_lock
from helper import label_results_from, send_email
from reg_exps import *


def issue_auth_token(res, token):
    """
    Reissues Authorization token for the user.

    NOTE: Only works on user that has been checked with validate_login().
    """
    if 'Bearer ' in token:
        token = token.replace('Bearer ', '', 1)
    old_token = jwt.decode(token, jwt_key, algorithms=config['jwt_alg'])
    new_token = jwt.encode({
        "iat": int(time.time()),
        "session": old_token['session'],
        "sub": old_token['sub'],
        "permission": old_token['permission']
    }, jwt_key, algorithm=config['jwt_alg'])
    res.set_cookie(
        "Authorization",
        "Bearer " + new_token,
        max_age=config["login_duration"]  ,
        domain="localhost",
        samesite="Lax"
        # secure=True,
        # httponly=True
    )


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


def validate_login(auth: str, permission=0):
    """
    Checks if a user has a valid login session, and has the necessary 
    permissions granted.

    NOTE:  For creating sequential "fail_no" (fail numbers), start at 8, as this
    function may produce fail numbers 1 through 7.

    :param auth:       The Authorization cookie given to the user.
    :param permission: Minimum permission level required (0=user, 1=admin)

    :type auth:       str
    :type permission: int

    :returns: True if login was authenticated, and if False, a dictionary with 
        the reason why authentication failed.
    """
    # TODO: later maybe track Origin header?
    try:
        assert type(auth) is not None, 'You need to pass a valid auth param to validate_login()'
        #assert type(origin) is not None, 'You need to pass a valid origin param to validate_login()'
        assert type(permission) is not None, 'You need to pass a valid permission param to validate_login()'
    except AssertionError:
        return {
            "status": "fail",
            "fail_no": 1,
            "message": "The Authorization header was not provided."
        }

    if 'Bearer' in auth:
        auth = auth.replace('Bearer ', '', 1)

    token = jwt.decode(auth, jwt_key, algorithms=config['jwt_alg'])
    t = int(time.time())

    if token['iat'] + config['login_duration'] < t:
        return {
            "status": "fail",
            "fail_no": "2",
            "message": "Session is expired. Please log in again.",
            "details": {
                "iat": token['iat'],
                "age": config['login_duration'],
                "time": t
            }
        }, 400, {"Content-Type": "application/json"}

    if token['permission'] < permission:
        return {
            "status": "fail",
            "fail_no": "3",
            "message": "You do not have high enough permissions to view this endpoint."
        }, 403, {"Content-Type": "application/json"}

    return True
