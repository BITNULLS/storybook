"""
password.py
    Routes beginning with /api/password/

Routes:
    /api/password/forgot
    /api/password/reset
"""

from flask import request
from flask import make_response
from flask import Blueprint
from flask import redirect

import cx_Oracle
import random
import string
import datetime
import bcrypt

from core.email import send_email
from core.db import connection, conn_lock
from core.reg_exps import *
from core.helper import sanitize_redirects

a_password = Blueprint('a_password', __name__)

# input email & check if email exists
@a_password.route("/api/password/forgot", methods=['POST'])
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

    res = None
    if 'redirect' in request.form:
        user_redirect_url = sanitize_redirects(request.form['redirect'])
        res = make_response(redirect(user_redirect_url))
    else:
        res = make_response({
            "status": "ok"
        })


# new password updates old password in USER_PROFILE & deletes the inserted row in PASSWORD_RESET
# check if both password fields match
@a_password.route("/api/password/reset", methods=['POST'])
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

    res = None
    if 'redirect' in request.form:
        user_redirect_url = sanitize_redirects(request.form['redirect'])
        res = make_response(redirect(user_redirect_url))
    else:
        res = make_response({
            "status": "ok"
        })
