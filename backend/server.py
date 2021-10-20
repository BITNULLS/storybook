from flask import Flask
from flask import request
from flask import Response
from flask import send_file
import re
import cx_Oracle
import json
import bcrypt
import uuid 
import datetime
import csv
import io

app = Flask(__name__)

# regexes
# they're faster compiled, and they can be used throughout
re_alphanumeric8 = re.compile(r"[a-zA-Z0-9]{8,}")
re_hex36dash = re.compile(r"[a-fA-F0-9]{36,38}")
re_email = re.compile(r"[^@]+@[^@]+\.[^@]+")

# database connection
print('Connecting to database...', end=' ')
oracle_lib_dir = None 
with open('data/oracle_dir.txt') as txtfile:
    for line in txtfile.readlines():
        oracle_lib_dir = str(line)
        break
assert oracle_lib_dir is not None 

cx_Oracle.init_oracle_client(lib_dir=oracle_lib_dir)

oracle_config = None

with open('data/oracle_key.json') as jsonfile:
    oracle_config = json.load(jsonfile)
assert oracle_config is not None

connection = cx_Oracle.connect(
    oracle_config['username'], 
    oracle_config['password'], 
    oracle_config['connect_string']
)
print('connected')

# server settings
config = None

with open('data/config.json') as jsonfile:
    config = json.load(jsonfile)
assert config is not None 

def validate_login(auth, id, origin=None, permission=0):
    """
    Checks if a user has a valid login session, and has the necessary 
    permissions granted.

    NOTE:  For creating sequential "fail_no" (fail numbers), start at 8, as this
    function may produce fail numbers 1 through 7.

    :param auth:       The Authorization cookie given to the user.
    :param id:         The ID of the user it gave in the request.
    :param origin:     The Origin header from the request.
    :param permission: Minimum permission level required (0=user, 1=admin)

    :type auth:       str
    :type id:         int
    :type permission: int

    :returns: True if login was authenticated, and if False, a dictionary with 
        the reason why authentication failed.
    """
    # TODO: later maybe track Origin header?
    try:
        assert type(auth) is not None
        assert type(id) is not None
        assert type(permission) is not None # this shouldn't fail since we provide it
    except AssertionError:
        return {
            "status": "fail",
            "fail_no": 1,
            "message": "Either the Authorization or Origin header, user ID, or permission level was not provided."
        }

    # TODO: later, maybe track origin header?
    """
    if origin != config["origin"]:
        return {
            "status": "fail",
            "fail_no": 2,
            "message": "Invalid origin; anti-CSRF policy."
        }
    """
    
    if re_hex36dash.match( id ) is None:
        return {
            "status": "fail",
            "fail_no": 3,
            "message": "The user ID (sub) provided was not valid."
        }
    
    cursor = connection.cursor()

    try:
        cursor.execute(
            "select p.admin, s.session_id, s.user_id, s.last_login, s.active from USER_SESSION s inner join USER_PROFILE p ON s.user_id = p.user_id where user_id='" + id + "'"
        )
    except cx_Oracle.Error as e:
        return {
            "status": "fail",
            "fail_no": 4,
            "message": "Error when querying database.",
            "database_message": str(e)
        }
    
    result = cursor.fetchone()
    if result is None:
        return {
            "status": "fail",
            "fail_no": 5,
            "message": "No user matches the ID that was passed."
        }
    
    # TODO: replace result[5] with the actual position of the auth column
    if result[1] != auth:
        return {
            "status": "fail",
            "fail_no": 6,
            "message": "The Authorization header provided was invalid."
        }
    
    # TODO: replace [8] for the same reason above
    if result[0] <= permission:
        return {
            "status": "fail",
            "fail_no": 7,
            "message": "The specified user does not have a high enough permission level to access this resource."
        }
    
    # TODO: make sessions expire because too much time passed
    #if result[3] 
    
    if result[4] == 0:
        return {
            "status": "fail",
            "fail_no": 8,
            "message": "User is logged out. Login in again."
        }
    
    return True 

# routes
@app.route("/")
def index():
    return {
        "status": "ok"
    }

@app.route("/login", methods=['POST'])
def login():
    # check that all expected inputs are received
    try:
        assert 'email' in request.form
        assert 'password' in request.form
    except AssertionError:
        return {
            "status": "fail",
            "fail_no": 1,
            "message": "Either the email or the password was not provided."
        }

    # sanitize inputs: make sure they're all alphanumeric, longer than 8 chars
    if re_email.match( request.form['email'] ) is None or \
        re_alphanumeric8.match( request.form['password'] ) is None:
        return {
            "status": "fail",
            "fail_no": 2,
            "message": "Either the email or the password failed a sanitize check. The POSTed fields should be alphanumeric, longer than 8 characters."
        }
    
    # all good, now query database
    email = (request.form['email']).lower().strip()

    cursor = connection.cursor()
    try:
        cursor.execute(
            "select * from USER_PROFILE where email='" + email + "'"
        )
    except cx_Oracle.Error as e:
        return {
            "status": "fail",
            "fail_no": 3,
            "message": "Error when querying database.",
            "database_message": str(e)
        }
    
    result = cursor.fetchone() 
    if result is None:
        return {
            "status": "fail",
            "fail_no": 4,
            "message": "No email matches what was passed."
        }
    
    #print(result)
    #print(result[8])
    if not bcrypt.checkpw( request.form['password'].encode('utf8'), result[8].encode('utf8') ):
        return {
            "status": "fail",
            "fail_no": 5,
            "message": "Password is incorrect."
        }
    
    user_id = result[10]
    session_id = str(uuid.uuid4()) # generate a unique token for a user
    
    try:
        cursor.execute(
            "update USER_SESSION set session_id='" + session_id + "', active=1 where user_id='" + str(user_id) + "'"
        )
    except cx_Oracle.Error as e:
        return {
            "status": "fail",
            "fail_no": 6,
            "message": "Error when updating database.",
            "database_message": str(e)
        }
    
    res = make_response({
        "status": "ok",
        "message": "Successfully authenticated",
        "sub": user_id
    })
    res.set_cookie(
        "Authorization", 
        session_id, 
        max_age=config["login_duration"],
        domain=config["origin"]
    )

    return res

@app.route("/logout", methods=['POST'])
def logout():
    # make sure the user is authenticated first
    vl = validate_login( 
        request.cookies.get('Authorization'), 
        request.form['sub'],
        #request.headers['Origin'],
        permission=0
    )
    if vl != True:
        return vl 
    
    cursor = connection.cursor()
    try:
        cursor.execute(
            "update USER_SESSION set active=0 where user_id=" + str(request.form['sub'])
        )
    except cx_Oracle.Error as e:
        return {
            "status": "fail",
            "fail_no": 8,
            "message": "Error when updating database.",
            "database_message": str(e)
        }

    return {
        "status": "ok"
    }
    
@app.route("/register", methods=['POST'])
def register():
    return {
        "...": "..."
    }

@app.route("/password/forgot", methods=['POST'])
def password_forgot(): 
    return {
        "...": "..."
    }

@app.route("/password/reset", methods=['POST'])
def password_reset():
    return {
        "...": "..."
    }

@app.route("/book", methods=['POST'])
def get_users_books():
    return {
        "...": "..."
    }

@app.route("/storyboard/page", methods=['POST'])
def storyboard_get_page():
    return {
        "...": "..."
    }

@app.route("/storyboard/action", methods=['POST'])
def storyboard_save_user_action():
    return {
        "...": "..."
    }

@app.route("/quiz/submit", methods=['POST'])
def quiz_submit_answer():
    return {
        "...": "..."
    }

@app.route("/admin/book/upload", methods=['POST'])
def admin_book_upload():
    return {
        "...": "..."
    }

@app.route("/admin/book/grant", methods=['POST'])
def admin_grant_user_book_access():
    return {
        "...": "..."
    }

@app.route("/admin/page/edit", methods=['POST'])
def admin_page_edit():
    return {
        "...": "..."
    }

@app.route("/admin/page/add", methods=['POST'])
def admin_page_add():
    return {
        "...": "..."
    }

def create_csv(query_results, headers):
    """
    method to export data to csv
    - parses headers and query table to create array of rows from table
    - returns csv-formatted string
    """

    # new string data equal to headers string
    data = headers + "\n"

    # add tuple data to data string
    for row in query_results:

        new_row = ""

        for column in row:

            if isinstance(column, datetime.date):
                # if object is datetime.date object, convert to string in format mm/dd/yy
                new_row += column.strftime('%m/%d/%Y')
            
            else:
                # make sure it is a string
                new_row += str(column)
        
            new_row += ","

        data = data + new_row + "\n"

    return data

@app.route("/admin/user_data", methods=['POST'])
def admin_download_user_data():
    """
    Exports user profile data to a csv file

    - Connects to database
    - Computes a select query to get user profile data
    - calls create_csv(query_results, headers) to create csv-formatted string
    - creates and returns csv file using csv-formatted string
    """

    # connect to database
    cursor = connection.cursor()

    # select query
    try:
        cursor.execute("\
        select user_profile.username, \
        user_profile.email, \
        user_profile.first_name, \
        user_profile.last_name, \
        user_profile.created_on, \
        user_profile.last_login, \
        school.school_name, \
        study.study_name from user_profile \
        inner join school on user_profile.school_id = school.school_id \
        inner join study on user_profile.study_id = study.study_id")

    except cx_Oracle.Error as e:
        return {
            "status": "fail",
            "fail_no": 4,
            "message": "Error when querying database.",
            "database_message": str(e)
        }

    # call create_csv to render csv-formatted string
    user_csv_string = create_csv(query_results = cursor, headers = "Username,Email,First Name,Last Name,Created On,Last Login,School")
    
    # close connection
    connection.close()

    try:
        return Response(user_csv_string, mimetype="text,csv",headers={"Content-disposition":"attachment;filename=user_data.csv"})
    except Exception as e:
        return {
            "status": "fail",
            "fail_no": 9,
            "message": "Error when sending csv file.",
            "database_message": str(e)
        }

@app.route("/admin/action_data", methods=['POST'])
def admin_download_action_data():
    """
    Exports user action data to a csv file

    - Connects to database
    - Computes a select query to get user profile data
    - calls create_csv(query_results, headers) to create csv-formatted string
    - creates and returns csv file using csv-formatted string
    """

    # connect to database
    cursor = connection.cursor()

    # select query
    try:
        cursor.execute(" \
        select user_profile.username, \
        action.current_page, \
        action.prev_page, \
        action.link, \
        action.occurred_on \
        from user_profile \
        inner join action on user_profile.user_id = action.user_id")

    except cx_Oracle.Error as e:
        return {
            "status": "fail",
            "fail_no": 4,
            "message": "Error when querying database.",
            "database_message": str(e)
        }

    # call create_csv to render csv-formatted string
    user_action_csv_string = create_csv(query_results = cursor, headers = "Username,Current Page,Previous Page,External Link,Date Action Occurred")

    # close connection
    connection.close()

    # create csv file from string and return
    try:
        return Response(user_action_csv_string, mimetype="text,csv",headers={"Content-disposition":"attachment;filename=action_data.csv"})
    except Exception as e:
        return {
            "status": "fail",
            "fail_no": 9,
            "message": "Error when sending csv file.",
            "database_message": str(e)
        }

@app.route("/admin/response_data", methods=['POST'])
def admin_download_response_data():
    
    """
    Exports user profile data to a csv file

    - Connects to database
    - Computes a select query to get user profile data
    - calls create_csv(query_results, headers) to create csv-formatted string
    - creates and returns csv file using csv-formatted string
    """

    # connect to database
    cursor = connection.cursor()
    
    # select query
    try:
        cursor.execute(" \
        select user_profile.username, \
        study.study_name, \
        book.book_name, \
        question.question, \
        answer.answer, \
        user_response.answered_on from user_profile \
        inner join study on user_profile.study_id = study.study_id \
        inner join book on study.study_id = book.book_id \
        inner join user_response on user_profile.user_id = user_response.user_id \
        inner join answer on user_response.answer_id = answer.answer_id \
        inner join question on answer.question_id = question.question_id")

    except cx_Oracle.Error as e:
        return {
            "status": "fail",
            "fail_no": 4,
            "message": "Error when querying database.",
            "database_message": str(e)
        }

    # call create_csv to render csv-formatted string
    user_response_csv_string = create_csv(query_results = cursor, headers = "Username,Study,Book,Question,User Answer,Date Answered On")

    # close connection
    connection.close()

    # create csv file from string and return
    try:
        return Response(user_response_csv_string, mimetype="text,csv",headers={"Content-disposition":"attachment;filename=response_data.csv"})
    except Exception as e:
        return {
            "status": "fail",
            "fail_no": 9,
            "message": "Error when sending csv file.",
            "database_message": str(e)
        }

