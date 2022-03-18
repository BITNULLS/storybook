from json.decoder import JSONDecoder
from edu_storybook import bucket, sensitive
from flask import Flask
from flask import request
from flask import Response
from flask import send_file
from flask import make_response
from datetime import date
import string
import random
from multiprocessing import Process, Pipe, Queue
from threading import Lock
import re
import cx_Oracle
import json
import bcrypt
import uuid
import jwt
import os
import time
import smtplib
import datetime
import csv
import hashlib
import sys
from datetime import date
from flask_cors import CORS
from pdf2image import convert_from_path
from threading import Lock
from flask_cors import CORS

ALLOWED_EXTENSIONS = {'pdf', 'ppt', 'pptx'}

# ==================================== setup ===================================

app = Flask(__name__)
CORS(app) 

# regexes
# they're faster compiled, and they can be used throughout
re_alphanumeric = re.compile(r"[a-zA-Z0-9]")
re_alphanumeric2 = re.compile(r"[a-zA-Z0-9]{2,}")
re_alphanumeric8 = re.compile(r"[a-zA-Z0-9]{8,}")
re_hex36dash = re.compile(r"[a-fA-F0-9]{36,38}")
re_hex36 = re.compile(r"[a-f0-9-]{36,}")  # for uuid.uuid4
re_hex32 = re.compile(r"[A-F0-9]{32,}")  # for Oracle guid()
re_email = re.compile(r"[^@]+@[^@]+\.[^@]+")
re_timestamp = re.compile(
    r"(\d{4})-(\d{1,2})-(\d{1,2}) (\d{2}):(\d{2}):(\d{2})")

# server settings to load in
config = sensitive.config

# domain
domain_name = sensitive.domain_name

# json web tokens key
jwt_key = sensitive.jwt_key

# database connection
print('Connecting to database...', end=' ')
oracle_lib_dir = None
with open(config['sensitives']['files']['oracle_dir']) as txtfile:
    for line in txtfile.readlines():
        oracle_lib_dir = str(line)
        break
assert oracle_lib_dir is not None and oracle_lib_dir != '', config['sensitives'][
    'folders']['oracle_dir'] + ' is empty, it needs the filepath to the Oracle Instant Client'

cx_Oracle.init_oracle_client(lib_dir=oracle_lib_dir)

oracle_configs = sensitive.oracle_config

connection = cx_Oracle.connect(
    oracle_configs['username'],
    oracle_configs['password'],
    oracle_configs['connect_string']
)
print('connected')

conn_lock = Lock()


# ================================ remove queue ================================



# =================================== routes ===================================







@app.route("/book", methods=['GET'])
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
            "SELECT BOOK_NAME, DESCRIPTION FROM BOOK "
            +"INNER JOIN BOOK_STUDY ON BOOK.BOOK_ID = BOOK_STUDY.BOOK_ID"
            +"INNER JOIN USER_STUDY ON BOOK_STUDY.STUDY_ID = USER_STUDY.STUDY_ID"
            +"WHERE user_study.user_id= '"+ token['sub'] +"'"
        )
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

@app.route("/storyboard/pagecount/<int:book_id_in>", methods=['GET'])
def storyboard_get_pagecount(book_id_in):
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
    except ValueError:
        return {
            "status": "fail",
            "fail_no": 2,
            "message": "The book_id failed a sanitize check. The POSTed fields should be an integer."
        }, 400, {"Content-Type": "application/json"}

    # goes into database and gets the bucket folder.
    # goes into bucket and then says I want this image from this folder.
    cursor = connection.cursor()

    try:
        # get folder that holds that book's images
        cursor.execute(
            "SELECT page_count FROM BOOK where book_id =" + str(book_id) )
    except cx_Oracle.Error as e:
        return {"status": "fail",
                "fail_no": 3,
                "message": "Error when updating database action",
                "database_message": str(e)
                }, 400, {"Content-Type": "application/json"}

    pagecount = cursor.fetchone()
    return {
        "pagecount": pagecount[0]
    } 






@app.route("/schools", methods=['GET'])
def get_schools():
    '''
    Return a list of schools in the same style/format/convention that admin_get_users() returns a list of users.
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
