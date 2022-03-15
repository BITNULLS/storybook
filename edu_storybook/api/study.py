"""
study.py
    Handle all study related GET, POST, PUT, DELETE

Route:
    /api/studies
"""

from flask import request
from flask import Blueprint
from flask import send_file

import cx_Oracle
import logging 

from core.auth import validate_login
from core.bucket import bucket
from core.config import config
from core.db import connection, conn_lock
from core.helper import label_results_from
from core.sensitive import jwt_key
from core.reg_exps import *

a_study = Blueprint('a_study', __name__)
a_study_log = logging.getLogger('api.study')

@a_study.route("/api/studies", methods=['GET'])
def get_studies():
    '''
    Return a list of studies in the same style/format/convention that 
    admin_get_schools() returns a list of users.
    '''

    # check to make sure you have a offset
    try:
        assert 'offset' in request.form
    except AssertionError:
        a_study_log.debug(
            'User did not provide an offset when requesting a list of studies'
        )
        return {
            "status": "fail",
            "fail_no": 1,
            "message": "offset was not provided."
        }, 400, {"Content-Type": "application/json"}

    # sanitize inputs: make sure offset is int
    try:
        offset = int(request.form['offset'])
    except ValueError:
        a_study_log.debug('User provided a non-int value for the offset parameter')
        return {
            "status": "fail",
            "fail_no": 2,
            "message": "offset failed a sanitize check. The POSTed field should be an integer."
        }, 400, {"Content-Type": "application/json"}

    # connect to database
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT STUDY.STUDY_ID, STUDY.STUDY_NAME, SCHOOL.SCHOOL_NAME " +
            "FROM STUDY INNER JOIN SCHOOL ON study.school_id = school.school_id ORDER BY study_id OFFSET "+ 
            request.form["offset"] +" ROWS FETCH NEXT 50 ROWS ONLY"
        )
        label_results_from(cursor)
    except cx_Oracle.Error as e:
        a_study_log.warning('Error when accessing database')
        a_study_log.warning(e)
        return {
            "status": "fail",
            "fail_no": 3,
            "message": "Error when accessing database.",
            "database_message": str(e)
        }, 400, {"Content-Type": "application/json"}

    studies = cursor.fetchall()

    return {
        "studies": studies
    }
