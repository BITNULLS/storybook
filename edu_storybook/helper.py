

ALLOWED_EXTENSIONS = {'pdf', 'ppt', 'pptx'}

def allowed_file(filename):
    """
    checks that a file extension is one of the allowed extensions, defined by ALLOWED_EXTENSIONS

    :param filename: name of file to be uploaded
    :returns: bool. True if file extension allowed, False if extension not allowed
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
        max_age=config["login_duration"]  ,
        domain="localhost",
        samesite="Lax"
        # secure=True,
        # httponly=True
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
    :return: Boolean on whether or not the email was sent.
    """
    if config['production'] == False:
        return True

    # Write Email
    to_line = "To: " + user_name + " <" + user_email + ">\n"
    from_line = "From: EDU Storybooks <edustorybooks@gmail.com>\n"
    reply_to_line = "Reply-To: " + admin_name + " <" + admin_email + ">\n"
    subject_line = "Subject: " + subject + "\n\n"
    body_lines = body
    email_text = to_line + from_line + reply_to_line + subject_line + body_lines

    # Email Command
    try:
        server = smtplib.SMTP(sensitive.smtp, sensitive.port)
        server.starttls(context=sensitive.context)
        server.login('edustorybooks@gmail.com', sensitive.email_password)
        server.sendmail("edustorybooks@gmail.com", user_email, email_text)
    except:
        print("Exception in Email Process")
        return False
    finally:
        del to_line
        del from_line
        del reply_to_line
        del subject_line
        del body_lines
        del email_text


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

