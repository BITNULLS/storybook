from flask import Flask
from flask import request
from flask import Response
from flask import send_file
from flask import make_response
import re
import cx_Oracle
import json
import bcrypt
import uuid 
import datetime
import csv
import io
import jwt
import os
import time

# ==================================== setup ===================================

app = Flask(__name__)

# regexes
# they're faster compiled, and they can be used throughout
re_alphanumeric8 = re.compile(r"[a-zA-Z0-9]{8,}")
re_hex32 = re.compile(r"[a-fA-F0-9]{32,33}")
re_email = re.compile(r"[^@]+@[^@]+\.[^@]+")

# server settings to load in
config = None

with open('data/config.json') as jsonfile:
    config = json.load(jsonfile)
assert config is not None, 'Could not find data/config.json file; Did you download it?'

for folder in config['sensitives']['folders']:
    folder_act = config['sensitives']['folders'][folder]
    assert os.path.isdir(folder_act), 'Missing a sensitive data folder: ' + folder_act
for file in config['sensitives']['files']:
    file_act = config['sensitives']['files'][file]
    assert os.path.isfile(file_act), 'Missing a sensitive data file: ' + file_act

# domain
domain_name = None
with open(config['sensitives']['files']['domain']) as txtfile:
    for line in txtfile.readlines():
        domain_name = str(line)
        break
assert domain_name is not None and domain_name != '', config['sensitives']['files']['domain_name'] + ' is empty; It should not be empty'

# json web tokens key
jwt_key = None
with open(config['sensitives']['files']['jwt_key']) as txtfile:
    for line in txtfile.readlines():
        jwt_key = str(line)
        break
assert jwt_key is not None and jwt_key != '', config['sensitives']['files']['jwt_key'] + ' is empty; It should not be empty'

# database connection
print('Connecting to database...', end=' ')
oracle_lib_dir = None 
with open(config['sensitives']['files']['oracle_dir']) as txtfile:
    for line in txtfile.readlines():
        oracle_lib_dir = str(line)
        break
assert oracle_lib_dir is not None and oracle_lib_dir != '', config['sensitives']['folders']['oracle_dir'] + ' is empty, it needs the filepath to the Oracle Instant Client'

cx_Oracle.init_oracle_client(lib_dir=oracle_lib_dir)

oracle_config = None

with open(config['sensitives']['files']['oracle_key']) as jsonfile:
    oracle_config = json.load(jsonfile)
assert oracle_config is not None, 'Oracle Key json was empty for some reason'

connection = cx_Oracle.connect(
    oracle_config['username'], 
    oracle_config['password'], 
    oracle_config['connect_string']
)
print('connected')

# ============================== helper functions ==============================

def label_results_from(cursor: cx_Oracle.Cursor):
    """
    Labels results from a cursor into a dictionary where like
    {
        "column1": "value1",
        "col2":    "val2",
        ...
    }
    I am amazed that cx_Oracle does not provide this. Labeling the columns in 
    the returned data is so basic. Why doesn't it do it. I checked the docs.
    Oracle thinks this is reasonable. I do not think this is reasonable, but 
    okay.

    :param cursor: A cursor that has been .execute[d].
    :type cursor: cx_Oracle.Cursor

    :returns: The same cursor with the row factory applied.
    """
    columns = [col[0] for col in cursor.description]
    cursor.rowfactory = lambda *args: dict(zip(columns, args))
    return cursor

def issue_auth_token(res, token):
    """
    Reissues Authorization token for the user.

    NOTE: Only works on user that has been checked with validate_login().
    """
    if 'Bearer ' in token:
        token = token.replace('Bearer ', '', 1)
    old_token = jwt.decode(token, jwt_key, algorithms=config['jwt_alg'])
    new_token = jwt.encode({
        "iat": int(time.time()),
        "session": old_token['session'],
        "sub": old_token['sub'],
        "permission": old_token['permission']
    }, jwt_key, algorithm=config['jwt_alg'])
    res.set_cookie(
        "Authorization", 
        "Bearer " + new_token, 
        max_age=config["login_duration"]#,
        #domain=domain_name,
        #secure=True,
        #httponly=True
    )

def send_email(user_name: str, user_email: str, admin_name: str, admin_email: str, subject: str, body: str) -> bool:
    """
    Creates and sends an email to a user
    :param user_name: The name of the user
    :param to_email: The email of the user
    :param admin_name: Admin of user's study
    :param admin_email: Admin's email
    :param subject: Subject of the email
    :param body: Body of the email; where actual text is placed
    :return: 
    """
    if config['production'] == False:
        return True

    # Write Email
    if not os.path.isdir('tmp'):
        os.mkdir('tmp')
    try:
        to_line = "To: " + user_name + " <" + user_email + ">\n"
        from_line = "From: EDU Storybooks <edustorybooks@gmail.com>\n"
        reply_to_line = "Reply-To: " + admin_name + " <" + admin_email + ">\n"
        subject_line = "Subject: " + subject + "\n"
        body_lines = body
        email_text = to_line + from_line + reply_to_line + subject_line + body_lines
        file_name = user_name + datetime.datetime.now().strftime("%m%d%Y%H%M%S") + ".txt"
        email = open("tmp/" + file_name, "w+")
        email.write(email_text)
        email.close

        #Email Command
        email_command = "ssmtp " + user_email + " < " + "tmp/" + file_name
        os.system(email_command)
        os.remove("tmp/" + file_name)
        del to_line
        del from_line
        del reply_to_line
        del subject_line
        del body_lines
        del email_text
        del file_name
        return True
    except:
        print("Exeption occurred during email process.")
        return False

def validate_login(auth: str, permission=0):
    """
    Checks if a user has a valid login session, and has the necessary 
    permissions granted.

    NOTE:  For creating sequential "fail_no" (fail numbers), start at 8, as this
    function may produce fail numbers 1 through 7.

    :param auth:       The Authorization cookie given to the user.
    :param permission: Minimum permission level required (0=user, 1=admin)

    :type auth:       str
    :type permission: int

    :returns: True if login was authenticated, and if False, a dictionary with 
        the reason why authentication failed.
    """
    # TODO: later maybe track Origin header?
    try:
        assert type(auth) is not None, 'You need to pass a valid auth param to validate_login()'
        #assert type(origin) is not None, 'You need to pass a valid origin param to validate_login()'
        assert type(permission) is not None, 'You need to pass a valid permission param to validate_login()'
    except AssertionError:
        return {
            "status": "fail",
            "fail_no": 1,
            "message": "The Authorization header was not provided."
        }

    if 'Bearer' in auth:
        auth = auth.replace('Bearer ', '', 1)

    token = jwt.decode(auth, jwt_key, algorithms=config['jwt_alg'])
    t = int(time.time())

    if token['iat'] + config['login_duration'] < t:
        return {
            "status": "fail",
            "fail_no": "2",
            "message": "Session is expired. Please log in again.",
            "details": {
                "iat": token['iat'],
                "age": config['login_duration'],
                "time": t
            }
        }, 400, {"Content-Type": "application/json"}
    
    if token['permission'] < permission:
        return {
            "status": "fail",
            "fail_no": "3",
            "message": "You do not have high enough permissions to view this endpoint."
        }, 403, {"Content-Type": "application/json"}
    
    return True 

# =================================== routes ===================================

@app.route("/")
def index():
    # revalidate login
    if 'Authorization' in request.cookies:
        # check if a user has valid credentials
        auth = request.cookies.get('Authorization')
        vl = validate_login( 
            auth, 
            permission=0
        )
        if vl != True:
            return vl
        
        res = make_response({
            "status": "ok",
            "login": "reverified"
        })
        issue_auth_token(res, auth)
        return res
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
        }, 400, {"Content-Type": "application/json"}

    # sanitize inputs: make sure they're all alphanumeric, longer than 8 chars
    if re_email.match( request.form['email'] ) is None or \
        re_alphanumeric8.match( request.form['password'] ) is None:
        return {
            "status": "fail",
            "fail_no": 2,
            "message": "Either the email or the password failed a sanitize check. The POSTed fields should be alphanumeric, longer than 8 characters."
        }, 400, {"Content-Type": "application/json"}
    
    # all good, now query database
    email = (request.form['email']).lower().strip()

    cursor = connection.cursor()
    try:
        cursor.execute(
            "select * from USER_PROFILE where email='" + email + "'"
        )
        label_results_from(cursor)
    except cx_Oracle.Error as e:
        return {
            "status": "fail",
            "fail_no": 3,
            "message": "Error when querying database.",
            "database_message": str(e)
        }, 400, {"Content-Type": "application/json"}
    
    result = cursor.fetchone() 
    if result is None:
        return {
            "status": "fail",
            "fail_no": 4,
            "message": "No email matches what was passed."
        }, 400, {"Content-Type": "application/json"}

    #print(result)
    #print(result[8])
    if not bcrypt.checkpw( request.form['password'].encode('utf8'), result['PASSWORD'].encode('utf8') ):
        return {
            "status": "fail",
            "fail_no": 5,
            "message": "Password is incorrect."
        }, 400, {"Content-Type": "application/json"}
    
    user_id = result['USER_ID']
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
        }, 400, {"Content-Type": "application/json"}
    
    iat = int(time.time())

    res = make_response({
        "status": "ok",
        "message": "Successfully authenticated",
        "iat": iat
    })
    token = jwt.encode({
        "iat": iat,
        "session": session_id,
        "sub": user_id,
        "permission": result['ADMIN']
    }, jwt_key, algorithm=config['jwt_alg'])
    res.set_cookie(
        "Authorization", 
        "Bearer " + token, 
        max_age=config["login_duration"],
        #domain=domain_name#, # TODO: uncomment in production
        #secure=True,
        #httponly=True
    )

    return res

@app.route("/logout", methods=['POST'])
def logout():
    # make sure the user is authenticated first
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
    
    cursor = connection.cursor()
    try:
        cursor.execute(
            "update USER_SESSION set active=0 where user_id='" + token['sub'] + "'"
        )
    except cx_Oracle.Error as e:
        return {
            "status": "fail",
            "fail_no": 8,
            "message": "Error when updating database.",
            "database_message": str(e)
        }

    res = make_response({
        "status": "ok"
    })
    res.set_cookie('Authorization', '', expires=0)
    return res
    
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

@app.route("/admin/user", methods=['POST'])
def admin_download_user_data():

    """
    Exports user profile data to a csv file

    - Connects to database
    - Computes a select query to get user profile data
    - calls create_csv(query_results, headers) to create csv-formatted string
    - creates and returns csv file using csv-formatted string
    """

    # validate that user can access data
    # vl = validate_login( 
    #     request.cookies.get('Authorization'), 
    #     request.form['sub'],
    #     #request.headers['Origin'],
    #     permission=0
    # )
    # if vl != True:
    #     return vl

    print("passed auth")
    # connect to database
    cursor = connection.cursor()

    # select query
    try:
        cursor.execute("select\
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

    # assign variable data to cursor.fetchall(). if i do not assign it to a variable, Response() sees it as an empty string
    data = cursor.fetchall()

    # column headers for csv
    headers = 'Username,Email,First Name,Last Name,Created On,Last Login,School\n'
   
    # create csv response object
    response = Response(headers + ''.join(list(map(lambda x: ",".join(tuple(map(lambda i: str(i), x))) + "\n", data))), mimetype="text,csv",headers={"Content-disposition":"attachment;filename=user_data.csv"})
    
    # close connection
    connection.close()

    try:
        return response

    except Exception as e:
        return {
            "status": "fail",
            "fail_no": 9,
            "message": "Error when sending csv file.",
            "flask_message": str(e)
        }

@app.route("/admin/action", methods=['POST'])
def admin_download_action_data():
    """
    Exports user action data to a csv file

    - Connects to database
    - Computes a select query to get user profile data
    - calls create_csv(query_results, headers) to create csv-formatted string
    - creates and returns csv file using csv-formatted string
    """

    # validate that user can access data
    # vl = validate_login( 
    #     request.cookies.get('Authorization'), 
    #     request.form['sub'],
    #     #request.headers['Origin'],
    #     permission=0
    # )
    # if vl != True:
    #     return vl

    # connect to database
    cursor = connection.cursor()

    # select query
    try:
        cursor.execute("select user_profile.email, \
        action.action_start, \
        action.action_stop, \
        book.book_name, \
        action_key.action_name, \
        action_detail.detail_description \
        from user_profile \
        inner join action on user_profile.user_id = action.user_id \
        inner join book on action.book_id = book.book_id \
        inner join action_detail on action_detail.detail_id = action.detail_id \
        inner join action_key on action_detail.action_id = action_key.action_id")

    except cx_Oracle.Error as e:
        return {
            "status": "fail",
            "fail_no": 4,
            "message": "Error when querying database.",
            "database_message": str(e)
        }

    # assign variable data to cursor.fetchall(). if i do not assign it to a variable, Response() sees it as an empty string
    data = cursor.fetchall()

    # column headers for csv
    headers = 'Email,Start,Stop,Book Name,Action,Details\n'
   
    # create csv response object
    response = Response(headers + ''.join(list(map(lambda x: ",".join(tuple(map(lambda i: str(i), x))) + "\n", data))), mimetype="text,csv",headers={"Content-disposition":"attachment;filename=user_data.csv"})
    
    # close connection
    connection.close()

    try:
        return response

    except Exception as e:
        return {
            "status": "fail",
            "fail_no": 9,
            "message": "Error when sending csv file.",
            "flask_message": str(e)
        }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)

