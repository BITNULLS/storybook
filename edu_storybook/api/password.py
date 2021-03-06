"""
password.py

Routes beginning with `/api/password/`.

Routes:

```
/api/password/forgot
/api/password/reset
```
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
import logging

from edu_storybook.core.email import send_email
from edu_storybook.core.db import pool
from edu_storybook.core.reg_exps import *
from edu_storybook.core.helper import sanitize_redirects
from edu_storybook.core.config import Config

a_password = Blueprint('a_password', __name__)

a_password_log = logging.getLogger('api.password')
if Config.production == False:
    a_password_log.setLevel(logging.DEBUG)

# input email & check if email exists
@a_password.route("/api/password/forgot", methods=['POST'])
def password_forgot():
    # checks for input
    try:
        assert 'email' in request.form
    except AssertionError:
        a_password_log.debug('Missing email in password forgot request.')
        return {
            "status": "fail",
            "fail_no": 1,
            "message": "Email was not provided."
        }, 400, {"Content-Type": "application/json"}

    # sanitize inputs: alphanumeric, > 8 chars
    if re_email.match(request.form['email']) is None:
        a_password_log.debug('Email form data failed sanitize check.')
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

    connection = pool.acquire()
    cursor = connection.cursor()

    try:
        cursor.execute(
            # fix the SQL statement with user_session?
            "SELECT * FROM USER_PROFILE WHERE EMAIL ='" + email + "'")
    except cx_Oracle.Error as e:
        a_password_log.warning('Error when accessing database')
        a_password_log.warning(e)
        return {
            "status": "fail",
            "fail_no": 3,
            "message": "Error when querying database.",
            "database_message": str(e)
        }, 400, {"Content-Type": "application/json"}

    result = cursor.fetchone()
    if result is None:
        a_password_log.debug('User requested a password forgot on an email that did not exist: ' + email)
        return {
            "status": "fail",
            "fail_no": 4,
            "message": "No email matches what was passed."
        }, 400, {"Content-Type": "application/json"}

    user_id = result[8]
    user_name = result[1] + ' ' + result[2]

    now = datetime.datetime.now()
    req_date = (now.strftime("%Y/%m/%d"))

    try:
        cursor.execute(
            "INSERT INTO PASSWORD_RESET(USER_ID, RESET_KEY, REQUEST_DATE) VALUES('" + user_id + "','" + rand_str + "', TO_DATE('" + req_date + "', 'yyyy/mm/dd'))")
        connection.commit()
    except cx_Oracle.Error as e:
        a_password_log.warning('Error when accessing database')
        a_password_log.warning(e)
        return {
            "status": "fail",
            "fail_no": 5,
            "message": "Error when querying database.",
            "database_message": str(e)
        }, 400, {"Content-Type": "application/json"}

    key = 'edustorybook.tk/password/reset#key=' + rand_str

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
    return res


@a_password.route("/api/password/reset", methods=['POST'])
def password_reset():
    '''
    New password updates old password in USER_PROFILE & deletes the inserted row
    in PASSWORD_RESET check if both password fields match
    '''
    # check expected input
    try:
        assert 'new_pass' in request.form
        assert 'confirm_pass' in request.form
        assert 'reset_key' in request.form
    except AssertionError:
        a_password_log.debug('User tried to reset a password without' +\
            'providing a new password, or reset key')
        return {
            "status": "fail",
            "fail_no": 1,
            "message": "Either password was not provided."
        }, 400, {"Content-Type": "application/json"}

    # sanitize inputs: make sure they're all alphanumeric, longer than 8 chars
    if re_password.match(request.form['new_pass']) is None or \
            re_password.match(request.form['confirm_pass']) is None:
        a_password_log.debug('User tried to reset password with invalid password')
        return {
            "status": "fail",
            "fail_no": 2,
            "message": "Either one or both passwords failed sanitization" +\
                " check of more than 8 characters &/or alphanumeric."
        }, 400, {"Content-Type": "application/json"}

    # check if both passwords match
    if (request.form['new_pass'] != request.form['confirm_pass']):
        a_password_log.debug('User tried to reset password with unmatched password')
        return {
            "status": "fail",
            "fail_no": 3,
            "message": "Both passwords do not match."
        }, 400, {"Content-Type": "application/json"}

    hashed = bcrypt.hashpw(
        request.form['confirm_pass'].encode('utf8'), bcrypt.gensalt())

    reset_key = (request.form['reset_key'])

    # connect to database
    connection = pool.acquire()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT USER_ID FROM PASSWORD_RESET WHERE RESET_KEY ='" + reset_key + "'")
    except cx_Oracle.Error as e:
        a_password_log.warning('Error when accessing database')
        a_password_log.warning(e)
        return {
            "status": "fail",
            "fail_no": 4,
            "message": "Error when querying database.",
            "database_message": str(e)
        }, 400, {"Content-Type": "application/json"}

    result = cursor.fetchone()
    if result is None:
        a_password_log.debug('User tried to reset a password with an invalid reset_key')
        return {
            "status": "fail",
            "fail_no": 5,
            "message": "No reset_key matches what was passed."
        }, 400, {"Content-Type": "application/json"}

    try:
        cursor.execute("UPDATE USER_PROFILE set PASSWORD ='" +
                       hashed.decode('utf8') + "' WHERE user_id ='" + result[0] + "'")
        connection.commit()
    except cx_Oracle.Error as e:
        a_password_log.warning('Error when accessing database')
        a_password_log.warning(e)
        return {
            "status": "fail",
            "fail_no": 6,
            "message": "Error when querying database.",
            "database_message": str(e)
        }, 400, {"Content-Type": "application/json"}

    try:
        cursor.execute(
            "DELETE FROM PASSWORD_RESET WHERE RESET_KEY ='" + reset_key + "'")
        connection.commit()
    except cx_Oracle.Error as e:
        a_password_log.warning('Error when accessing database')
        a_password_log.warning(e)
        return {
            "status": "fail",
            "fail_no": 7,
            "message": "Error when querying database.",
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
