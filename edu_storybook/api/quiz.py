"""
quiz.py
    Routes beginning with /api/quiz/

Routes:
    /api/quiz/submit
"""

from flask import request
from flask import Blueprint

import jwt
import cx_Oracle
import logging

from edu_storybook.core.helper import label_results_from
from edu_storybook.core.auth import validate_login, issue_auth_token
from edu_storybook.core.config import config
from edu_storybook.core.db import connection, conn_lock
from edu_storybook.core.sensitive import jwt_key
from edu_storybook.core.reg_exps import *

a_quiz = Blueprint('a_quiz', __name__)

a_quiz_log = logging.getLogger('api.quiz')
if config['production'] == False:
    a_quiz_log.setLevel(logging.DEBUG)

@a_quiz.route("/api/quiz/submit", methods=['POST'])
def quiz_submit_answer():
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

    try:
        assert 'answer_id' in request.form
        assert 'question_id' in request.form
    except AssertionError:
        a_quiz_log.debug('User submitted a quiz response without an answer and/or question ID')
        return {
            "status": "fail",
            "fail_no": 1,
            "message": "Either the answer_id or the question_id was not provided."
        }, 400, {"Content-Type": "application/json"}

    try:
        answer_id = int(request.form['answer_id'])
        question_id = int(request.form['question_id'])
    except ValueError:
        a_quiz_log.debug('User submitted a quiz response that was malformed')
        return {
            "status": "fail",
            "fail_no": 2,
            "message": "Either the answer_id or the question_id contained invalid characters."
        }, 400, {"Content-Type": "application/json"}
    
    token = jwt.decode(auth, jwt_key, algorithms=config['jwt_alg'])
    
    cursor = connection.cursor()
    
    try:
        conn_lock.acquire()
        cursor.execute(
            "insert into user_response (user_id, question_id, answer_id, answered_on) values (" + "'" +
            token['sub'] + "', " + str(question_id) +
            ", " + str(answer_id) + ", current_timestamp)"
        )
        connection.commit()
    except cx_Oracle.Error as e:
        a_quiz_log.warning('Error when accessing database')
        a_quiz_log.warning(e)
        return {
            "status": "fail",
            "fail_no": 3,
            "message": "Error when updating database.",
            "database_message": str(e)
        }, 400, {"Content-Type": "application/json"}
    finally:
        conn_lock.release()
        
    try:
       conn_lock.acquire()
       cursor.execute(
           "SELECT correct FROM answer WHERE answer_id= " + str(answer_id) + " and question_id= " + str(question_id)
       )
       label_results_from(cursor)
       connection.commit()
    except cx_Oracle.Error as e:
        a_quiz_log.warning('Error when accessing database')
        a_quiz_log.warning(e)
        return {
            "status": "fail",
            "fail_no": 4,
            "message": "Error when updating database.",
            "database_message": str(e)
        }, 400, {"Content-Type": "application/json"}
    finally:
        conn_lock.release()

    result = cursor.fetchone()

    if result['CORRECT']:
        return {
           "status": "ok",
           "correct": True
        }
    elif ~result['CORRECT']:
        return {
           "status": "ok",
           "correct": False
        }
    return {
           "status": "fail",
           "fail_no": 7,
           "message": "No choice matches what was passed."
        }, 400, {"Content-Type": "application/json"}
