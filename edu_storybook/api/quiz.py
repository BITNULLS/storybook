"""
quiz.py

Routes beginning with `/api/quiz/`.

Routes:

```
/api/quiz/submit
```
"""

from flask import request
from flask import Blueprint
from flask import redirect

import jwt
import cx_Oracle
import logging

from edu_storybook.core.helper import label_results_from
from edu_storybook.core.auth import validate_login, issue_auth_token
from edu_storybook.core.config import Config
from edu_storybook.templates import Templates
from edu_storybook.api.storyboard import check_quiz_question
from edu_storybook.core.db import pool
from edu_storybook.core.sensitive import jwt_key
from edu_storybook.core.reg_exps import *

a_quiz = Blueprint('a_quiz', __name__)

a_quiz_log = logging.getLogger('api.quiz')
if Config.production == False:
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
        assert 'type' in request.form
        assert 'question_id' in request.form
    except AssertionError:
        a_quiz_log.debug('User submitted a quiz response without specifying' +\
            ' the type or question ID')
        return {
            "status": "fail",
            "fail_no": 4,
            "message": "Either the type or the question_id was not provided."
        }, 400, {"Content-Type": "application/json"}

    if request.form['type'] == 'mc':
        try:
            assert 'answer_id' in request.form
        except AssertionError:
            a_quiz_log.debug('User submitted a multiple choice quiz response' +\
                ' without specifying the answer ID')
            return {
                "status": "fail",
                "fail_no": 5,
                "message": "The answer_id was not provided."
            }, 400, {"Content-Type": "application/json"}
    elif request.form['type'] == 'fr':
        try:
            assert 'answer' in request.form
        except AssertionError:
            a_quiz_log.debug('User submitted a multiple choice quiz response' +\
                ' without specifying their answer')
            return {
                "status": "fail",
                "fail_no": 6,
                "message": "The answer was not provided."
            }, 400, {"Content-Type": "application/json"}
    else:
        return {
            "status": "fail",
            "fail_no": 7,
            "message": "An invalid question type was provided, should only" +\
                " be mc (multiple choice) or fr (free response)"
        }, 400, {"Content-Type": "application/json"}

    question_id = None
    answer_id = None

    try:
        question_id = int(request.form['question_id'])
        if request.form['type'] == 'mc':
            answer_id = int(request.form['answer_id'])
    except ValueError:
        a_quiz_log.debug('User submitted a quiz response that was malformed')
        return {
            "status": "fail",
            "fail_no": 8,
            "message": "Either the answer_id or the question_id contained" +\
                "invalid characters."
        }, 400, {"Content-Type": "application/json"}

    token = jwt.decode(auth, jwt_key, algorithms=Config.jwt_alg)

    connection = pool.acquire()
    cursor = connection.cursor()

    if request.form['type'] == 'mc': # multiple choice handling
        
        try:
            cursor.execute(
                "SELECT correct, answer_feedback FROM answer WHERE answer_id= " + str(answer_id) +\
                    " and question_id= " + str(question_id)
            )
            label_results_from(cursor)
            connection.commit()
        except cx_Oracle.Error as e:
            a_quiz_log.warning('Error when accessing database')
            a_quiz_log.warning(e)
            return {
                "status": "fail",
                "fail_no": 9,
                "message": "Error when accessing database.",
                "database_message": str(e)
            }, 400, {"Content-Type": "application/json"}

        result = cursor.fetchone()
        
        try:
            cursor.execute(
                "insert into user_response (user_id, question_id, answer_id, answered_on) values (" + "'" +
                    token['sub'] + "', " + str(question_id) +
                    ", " + str(answer_id) + ", current_timestamp)"
                )
            connection.commit()
        except cx_Oracle.Error as e:
            a_quiz_log.warning('Error when updating database')
            a_quiz_log.warning(e)
                
            return {
                "status": "fail",
                "fail_no": 10,
                "message": "Error when updating database.",
                "database_message": str(e)
            }, 400, {"Content-Type": "application/json"}
            

        if result['CORRECT']:
            feedback_page = Templates._base.substitute(
                title = "Feedback Page",
                description = "This page is meant to provide feedback to users",
                body = Templates.storyboard_quiz_feedback.substitute(
                    feedback = result['ANSWER_FEEDBACK'],
                    page_redirection = request.form['redirect'],
                    tryAgainBtnVisibility = "display: none",
                    continueBtnVisibility = "display: block"   
                )
            )
        elif ~result['CORRECT']:
            feedback_page = Templates._base.substitute(
                title = "Feedback Page",
                description = "This page is meant to provide feedback to users",
                body = Templates.storyboard_quiz_feedback.substitute(
                    feedback = result['ANSWER_FEEDBACK'],
                    page_redirection = request.form['redirect'],
                    tryAgainBtnVisibility = "display: block",
                    continueBtnVisibility = "display: none"   
                )
            )
        return feedback_page
    
    elif request.form['type'] == 'fr': # free response handling
        free_response_answer = request.form['answer']
        try:
            cursor.execute(
                "insert into user_free_response (user_id, question_id, response, submitted_on) values (" + "'" +
                token['sub'] + "', " + str(question_id) +
                ", " + "'" + free_response_answer + "', current_timestamp)"
            )
            connection.commit()
        except cx_Oracle.Error as e:
            a_quiz_log.warning('Error when accessing database')
            a_quiz_log.warning(e)
            return {
                "status": "fail",
                "fail_no": 9,
                "message": "Error when updating database.",
                "database_message": str(e)
            }, 400, {"Content-Type": "application/json"}

        return redirect(request.form['redirect'])
        
    else:
        return {
            "status": "fail",
            "fail_no": 12,
            "message": "This should be unreachable"
            }, 400, {"Content-Type": "application/json"}
