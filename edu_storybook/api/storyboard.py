"""
storyboard.py

Routes beginning with `/api/storyboard/`.

Routes:

```
/api/storyboard/page/<int:book_id_in>/<int:page_number_in>
/api/storyboard/pagecount/<int:book_id_in>
/api/storyboard/cover/<int:book_id_in>
```
"""

from flask import request
from flask import Blueprint
from flask import send_file

import jwt
import cx_Oracle
import logging

from edu_storybook.core.auth import validate_login
from edu_storybook.core.bucket import download_bucket_file
from edu_storybook.core.config import Config, temp_folder
from edu_storybook.core.db import pool
from edu_storybook.core.helper import label_results_from
from edu_storybook.core.sensitive import jwt_key
from edu_storybook.core.reg_exps import *

a_storyboard = Blueprint('a_storyboard', __name__)

a_storyboard_log = logging.getLogger('api.storyboard')
if Config.production == False:
    a_storyboard_log.setLevel(logging.DEBUG)

@a_storyboard.route("/api/storyboard/page/<int:book_id_in>/<int:page_number_in>", methods=['GET'])
def storyboard_get_page(book_id_in: int, page_number_in: int):
    '''
    Gets a single page of the a book. If there is a question that a user must
    answer before opening a page, that question will be presented until the user
    answers the question.

    Expects:
     - book_id_in (URL parameter): The ID of the book being requested.
     - page_number_in (URL parameter): The page number of the book being
     requested.

    Fails:
     - `1` to `3`: Validate login errors
     - `4`: Either `book_id_in` or `page_number_in` failed a sanitize check.
     - `5`: Error accessing database for quiz questions.
     - `6`: Could not get image file of book page.

    Returns: Either the image of the book page as JPEG or PNG, or a quiz
    question in JSON, arranged as

    ```
    {
        "status": "ok",
        "question_id" : 1,
        "question" : "What is red?",
        "options" : [
            "A color",
            "Something",
            "Something else",
            ...
        ],
        "correct_answer": 2
    }
    ```
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

    # TODO: Token is not checked
    token = jwt.decode(auth, jwt_key, algorithms=Config.jwt_alg)

    # sanitize inputs: make sure book_id, page_number are ints
    try:
        book_id = int(book_id_in)
        page_number = int(page_number_in)
    except ValueError:
        a_storyboard_log.warning('This should not even be possible. ' +
            'A user HTTP GET non-int values to an int endpoint')
        return {
            "status": "fail",
            "fail_no": 4,
            "message": "The book_id or page_number failed a sanitize check." +\
                "The POSTed fields should be an integer."
        }, 400, {"Content-Type": "application/json"}

    # goes into database and gets the bucket folder.
    # goes into bucket and then says I want this image from this folder.
    connection = pool.acquire()
    cursor = connection.cursor()

    fileInput = get_book_image_path(book_id, page_number)
        
    quiz_questions = check_quiz_question(book_id, page_number, token['sub'])
    
    if(quiz_questions != False):
        # If there's a quiz question(s) for user to answer, then return the data for the first quiz question
        # for user to answer
        return quiz_questions[0]
    
    cursor = connection.cursor()
    try:
        cursor.callproc("track_last_page",\
            [token['sub'],\
            book_id_in,\
            page_number_in,\
            token['permission']])
        # commit changes to db
        connection.commit()
    except cx_Oracle.Error as e:
        a_storyboard_log.warning('Error when accessing the database')
        a_storyboard_log.warning(e)
        return {
            "status": "fail",
            "fail_no": 6,
            "message": "Error when querying database.",
            "database_message": str(e)
        }, 400, {"Content-Type": "application/json"}

    # Return page assuming current page has no quiz question
    try:
        return send_file(download_bucket_file(fileInput, folder=temp_folder))
    except Exception as e:
        a_storyboard_log.warning('Could not load bucket file for some unknown reason')
        a_storyboard_log.warning(e)
        return {
            "status": "fail",
            "fail_no": 6,
            "message": "Could not get image"
        }, 400, {"Content-Type": "application/json"}


def get_last_page(book_id_in: int, user_id_in: str):
    '''
     Gets the last page_number for a book with a given book_id and user_id
    '''
    
    book_id = str(book_id_in)
    
    # connect to database
    connection = pool.acquire()
    cursor = connection.cursor()
    
    try:
        cursor.execute(
            "SELECT DISTINCT BOOK.BOOK_ID, BOOK_NAME, DESCRIPTION, LAST_PAGE.LAST_PAGE FROM BOOK "+
            "INNER JOIN BOOK_STUDY ON BOOK.BOOK_ID = BOOK_STUDY.BOOK_ID "+
            "INNER JOIN USER_STUDY ON BOOK_STUDY.STUDY_ID = USER_STUDY.STUDY_ID "+
            "INNER JOIN LAST_PAGE ON LAST_PAGE.BOOK_ID = BOOK.BOOK_ID "+
            "WHERE user_study.user_id= '" + user_id_in + "' AND last_page.book_id = " + book_id + " AND last_page.user_id = '" + user_id_in + "'"
        )
        label_results_from(cursor)
    except cx_Oracle.Error as e:
        a_storyboard_log.warning('Error when acessing database')
        a_storyboard_log.warning(e)
        return {
            "status": "fail",
            "fail_no": 4,
            "message": "Error when accessing books.",
            "database_message": str(e)
        }
    
    result = cursor.fetchone()
    
    if result is None:
        try:
            cursor.execute(
                "SELECT DISTINCT BOOK.BOOK_ID, BOOK_NAME, DESCRIPTION, 2 AS LAST_PAGE FROM BOOK "+
                "INNER JOIN BOOK_STUDY ON BOOK.BOOK_ID = BOOK_STUDY.BOOK_ID "+
                "INNER JOIN USER_STUDY ON BOOK_STUDY.STUDY_ID = USER_STUDY.STUDY_ID "
                "WHERE user_study.user_id= '" + user_id_in + "' AND book.book_id = " + book_id
            )
            label_results_from(cursor)
        except cx_Oracle.Error as e:
            a_storyboard_log.warning('Error when acessing database')
            a_storyboard_log.warning(e)
            return {
                "status": "fail",
                "fail_no": 4,
                "message": "Error when accessing books.",
                "database_message": str(e)
            }
            
        result = cursor.fetchone()

    return result['LAST_PAGE']

def check_quiz_question(book_id: int, page_number: int, user_id: str):
    '''
    This is the logic for checking if there's a quiz question(s) for a book with given book_id and given current
    page number page_number
    
    Parameters: book_id (int) - ID of the book
                page_number(int) - Current page number of a book
                user_id(str) - User ID
    
    Return: list of quiz question(s) OR boolean value False if there's no quiz question OR Oracle Error
            for not accessing quiz questions from DB correctly
    '''
    
    # goes into database and gets the bucket folder.
    # goes into bucket and then says I want this image from this folder.
    connection = pool.acquire()
    cursor = connection.cursor()
    
    try:
        # gets the unanswered quiz questions for a user (checks the user_response and user_free_response tables for which questions are answered)
        result = cursor.var(cx_Oracle.CURSOR)
        cursor.callproc("GET_QUIZ_QUESTIONS", \
            [book_id, page_number, user_id, result])
        
        # label_results_from(result)
    except cx_Oracle.Error as e:
        a_storyboard_log.warning('Error when acessing database')
        a_storyboard_log.warning(e)
        return {
            "status": "fail",
            "fail_no": 5,
            "message": "Error accessing quiz questions and its answers"
        }, 400, {"Content-Type": "application/json"}
        
    quizQuestions = result.getvalue().fetchall() # List of Tuples where each Tuple is one record from database and List would include all the records
    
    answers = []
    curr_question_id = None
    full_question = None
    question_type = None
    correct_answer = None
    quiz_question_list = []
    
    for question in quizQuestions:
        '''
        For each question in a tuple format, following is the mapping of index to column name:
        0: Retrieves QUESTION_ID
        1: Retrieves QUESTION
        2: Retrieves QUESTION_TYPE
        3: Retrives ANSWER_ID
        4: Retrieves ANSWER
        5: Retrieves CORRECT
        '''
        if curr_question_id == None:
            curr_question_id = question[0]
            full_question = question[1]
            question_type = question[2]
            answers.append({
                "answer": question[4],
                "answer_id": question[3],
                "is_correct": question[5]
            })
            if question[5] == 1:
                correct_answer = question[4]
        
        # This would mean that the question is a MC that has different options coming along        
        elif question[0] == curr_question_id:
            answers.append({
                "answer": question[4],
                "answer_id": question[3],
                "is_correct": question[5]
            })
            if question[5] == 1:
                correct_answer = question[4]
        
        # This means that new question came along
        # Save the output of previous question into quiz_question_list and free the variables to use for
        # upcoming question
        else:
            quiz_question_list.append(
                {
                    "question_id": curr_question_id,
                    "question": full_question,
                    "question_type": question_type,
                    "answers": answers,
                    "correct_answer": correct_answer
                }
            )
            
            # Reinitializing possible answers list and correct answer for next question
            answers = []
            correct_answer = None
            
            curr_question_id = question[0]
            full_question = question[1]
            question_type = question[2]
            answers.append({
                "answer": question[4],
                "answer_id": question[3],
                "is_correct": question[5]
            })
            if question[5] == 1:
                correct_answer = question[4]
            
            
    if(len(quiz_question_list) > 0 or curr_question_id != None):
        
        # Make sure to append the last question from quizQuestions since the loop would stop without adding
        # that last question
        
        quiz_question_list.append(
            {
                "question_id": curr_question_id,
                "question": full_question,
                "question_type": question_type,
                "answers": answers,
                "correct_answer": correct_answer
            }
        )
        return quiz_question_list
    
    else:
        return False
    
@a_storyboard.route("/api/storyboard/pagecount/<int:book_id_in>", methods=['GET'])
def storyboard_get_pagecount(book_id_in: int):
    '''
    Get the page count of a book.

    Expects:
     - book_id_in (URL parameter): The ID of the book.

    Returns: A JSON like `{"page_count": 48}`
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

    # TODO: verify token
    token = jwt.decode(auth, jwt_key, algorithms=Config.jwt_alg)

    # sanitize inputs: make sure book_id, page_number are ints
    try:
        book_id = int(book_id_in)
    except ValueError:
        a_storyboard_log.warning(
            'User provided an invalid book_id for storyboard_get_pagecount'
        )
        return {
            "status": "fail",
            "fail_no": 2,
            "message": "The book_id failed a sanitize check. The POSTed fields should be an integer."
        }, 400, {"Content-Type": "application/json"}

    # goes into database and gets the bucket folder.
    # goes into bucket and then says I want this image from this folder.
    connection = pool.acquire()
    cursor = connection.cursor()

    try:
        # get folder that holds that book's images
        cursor.execute(
            "SELECT page_count FROM BOOK where book_id =" + str(book_id) )
    except cx_Oracle.DatabaseError as e:
        a_storyboard_log.warning('Error when accessing database')
        a_storyboard_log.warning(e)
        return {
            "status": "fail",
            "fail_no": 3,
            "message": "Error when accessing database",
            "database_message": str(e)
        }, 400, {"Content-Type": "application/json"}

    pagecount = cursor.fetchone()
    return {
        "pagecount": pagecount[0]
    }


@a_storyboard.route("/api/storyboard/action", methods=['POST'])
def storyboard_save_user_action():
    '''
    Saves a user action.
    '''
    # Code the storyboard_save_user_action() function in the same style as logout()
    # Screenshot a successful POST request to the /storyboard/action endpoint.
    # Add to the backend/API.md the relevant documentation for the
    # /storyboard/action endpoint in the same style as the login/ endpoint
    # documentation.
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

    # TODO: verify token
    token = jwt.decode(auth, jwt_key, algorithms=Config.jwt_alg)

    # check that all expected inputs are received
    try:
        assert 'book_id' in request.form
        assert 'detail_description' in request.form
        assert 'action_key_id' in request.form
        assert 'action_start' in request.form
        assert 'action_stop' in request.form
    except AssertionError:
        a_storyboard_log.warning(
            'User did not provide one of the form values for storyboard_save_user_action'
        )
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
        a_storyboard_log.warning('User provided an invalid action data')
        return {
            "status": "fail",
            "fail_no": 3,
            "message": "Either the action_start, action_stop, or detail_description failed a sanitize check. The POSTed fields should be in date format YYYY-MM-DD HH:MM:SS. detail_description should be alphanumeric only."
        }, 400, {"Content-Type": "application/json"}

    connection = pool.acquire()
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
        a_storyboard_log.warning('Error when accessing database')
        a_storyboard_log.warning(e)
        return{
            "status": "fail",
            "fail_no": 4,
            "message": "Error when updating database action",
            "database_message": str(e)
        }, 400, {"Content-Type": "application/json"}
    return {
        "status": "ok"
    }


def get_book_image_path(book_id, page_number):
    '''
    Get the filepath of a book image in the bucket.

    Expects:
     - book_id: The ID of the book.
     - page_number: The page number in the book.

    Returns: A filepath like `1294912_book1_images/1294912_book1_3.png` which
    can be used in the `edu_storybook.core.bucket` module.
    '''
    connection = pool.acquire()
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
    return (fileInput + '_images/' + fileInput + '_' + str(page_number) + '.png')


@a_storyboard.route("/api/storyboard/cover/<int:book_id_in>", methods=['GET'])
def storyboard_get_cover_image(book_id_in):
    '''
    Get the cover image of a book.

    Expects:
     - book_id_in (URL parameter): The ID of the book being requested.

    Returns: The image of the first page of the book.
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

    try:
        book_id_in = int(book_id_in)
    except ValueError:
        return {
            "status": "fail",
            "fail_no": 2,
            "message": "The book_id or page_number failed a sanitize check. The POSTed fields should be an integer."
        }, 400, {"Content-Type": "application/json"}

    return send_file(download_bucket_file(get_book_image_path(book_id_in, 1), folder=temp_folder))
