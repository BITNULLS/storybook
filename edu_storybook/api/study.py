"""
study.py

Handle all study related GET, POST, PUT, DELETE operations.

Routes:

```
/api/studies/<int:offset>
```
"""

from flask import request
from flask import Blueprint
from flask import send_file

import cx_Oracle
import logging

from edu_storybook.core.auth import validate_login
from edu_storybook.core.bucket import bucket
from edu_storybook.core.config import Config
from edu_storybook.core.db import pool
from edu_storybook.core.helper import label_results_from
from edu_storybook.core.sensitive import jwt_key
from edu_storybook.core.reg_exps import *

a_study = Blueprint('a_study', __name__)

a_study_log = logging.getLogger('api.study')
if Config.production == False:
    a_study_log.setLevel(logging.DEBUG)

@a_study.route("/api/studies/<int:offset>", methods=['GET'])
def get_studies(offset):
    '''
    Return a list of studies in the same style/format/convention that
    admin_get_schools() returns a list of users.

    Expects:
     - offset (URL parameter): From 0 onward, how far to look into the studies
     table.

    Fails:
     - `1` to `3`: Validate login errors.
     - `5`: offset failed sanitize check.
     - `6`: Error when accessing database

    Returns: A list of studies, as

    ```
    {
        "studies": [
            {
                "STUDY_ID": 1,
                "STUDY_NAME": "Cool Study",
                "SCHOOL_NAME": "University of Delaware
            },
            ...
        ]
    }
    ```
    '''
    # validate that user has rights to access
    auth = request.cookies.get('Authorization')
    vl = validate_login(
        auth,
        permission=0
    )
    if vl != True:
        return vl

    if 'Bearer ' in auth:
        auth = auth.replace('Bearer ', '', 1)

    # sanitize inputs: make sure offset is int
    try:
        offset = int(offset)
    except ValueError:
        a_study_log.debug('User provided a non-int value for the offset parameter')
        return {
            "status": "fail",
            "fail_no": 5,
            "message": "offset failed a sanitize check. The POSTed field should be an integer."
        }, 400, {"Content-Type": "application/json"}

    # connect to database
    connection = pool.acquire()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT STUDY.STUDY_ID, STUDY.STUDY_NAME, SCHOOL.SCHOOL_NAME " +
            "FROM STUDY INNER JOIN SCHOOL ON study.school_id = school.school_id ORDER BY study_id OFFSET "+ 
            str(offset) +" ROWS FETCH NEXT 50 ROWS ONLY"
        )
        label_results_from(cursor)
    except cx_Oracle.Error as e:
        a_study_log.warning('Error when accessing database')
        a_study_log.warning(e)
        return {
            "status": "fail",
            "fail_no": 6,
            "message": "Error when accessing database.",
            "database_message": str(e)
        }, 400, {"Content-Type": "application/json"}

    studies = cursor.fetchall()

    return {
        "studies": studies
    }
