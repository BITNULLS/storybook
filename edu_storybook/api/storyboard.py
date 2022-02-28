"""
storyboard.py
    Routes beginning with /api/storyboard/

Routes:
    /api/storyboard/page/<int:book_id_in>/<int:page_number_in>
    /api/storyboard/action
"""

from flask import request
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
import time

from core.auth import validate_login
from core.bucket import bucket
from core.config import config
from core.db import connection, conn_lock
from core.sensitive import jwt_key
from core.reg_exps import *

a_storyboard = Blueprint('a_storyboard', __name__)

@a_storyboard.route("/api/storyboard/page/<int:book_id_in>/<int:page_number_in>", methods=['GET'])
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


@a_storyboard.route("/api/storyboard/action", methods=['POST'])
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
