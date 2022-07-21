"""
static_page.py

Just loads static_pages.

Routes:

```
/api/static_page/<int:id_in>
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

from markdown2 import Markdown

a_study = Blueprint('a_static_page', __name__)

a_static_page_log = logging.getLogger('api.study')
if Config.production == False:
    a_static_page_log.setLevel(logging.DEBUG)

@a_study.route("/api/static_page/<int:id>", methods=['GET'])
def get_static_page(id: int):
    '''
    Grab a static page and render it into HTML.
    '''
    # validate that user has rights to access
    connection = pool.acquire()
    cursor = connection.cursor()

    try:
        # get folder that holds that book's images
        cursor.execute(
            "SELECT * FROM static_page WHERE book_id =" + str(book_id) )
    except cx_Oracle.DatabaseError as e:
        a_static_page_log.warning('Error when accessing database')
        a_static_page_log.warning(e)
        return {
            "status": "fail",
            "fail_no": 3,
            "message": "Error when accessing database",
            "database_message": str(e)
        }, 400, {"Content-Type": "application/json"}

    pagecount = cursor.fetchone()
