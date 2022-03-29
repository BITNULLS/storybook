"""
auth.py
    ...

Functions:
    login()
    logout()
    register()
"""

import jwt
import time
import bcrypt
import uuid
import cx_Oracle
import logging
from flask import make_response

from .sensitive import jwt_key
from .config import config
from .helper import label_results_from
from .email import send_email
from .reg_exps import *

c_auth_log = logging.getLogger('core.auth')
if config['production'] == False:
    c_auth_log.setLevel(logging.DEBUG)


def issue_auth_token(res, token):
    """
    Reissues Authorization token for the user.

    :param res: A Flask response object.
    :param token: Old token to be refreshed.

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
        max_age=config["login_duration"],
        domain="localhost",
        samesite="Lax"
        # secure=True,
        # httponly=True
    )


def validate_login(auth: str, permission: int=0):
    """
    Checks if a user has a valid login session, and has the necessary
    permissions granted.

    NOTE:  For creating sequential "fail_no" (fail numbers), start at 8, as this
    function may produce fail numbers 1 through 7.

    Args:
     - auth (str): The Authorization cookie given to the user.
     - permission (int): Minimum permission level required (0=user, 1=admin)

    Returns:
        True if login was authenticated, and if False, a dictionary with the
        reason why authentication failed.
    """
    # TODO: later maybe track Origin header?
    try:
        assert auth is not None, 'You need to pass a valid auth param to validate_login()'
        #assert type(origin) is not None, 'You need to pass a valid origin param to validate_login()'
        assert permission is not None, 'You need to pass a valid permission param to validate_login()'
    except AssertionError:
        c_auth_log.debug('A user tried to use an endpoint without providing an Authorization header')
        return {
            "status": "fail",
            "fail_no": 1,
            "message": "The Authorization header was not provided."
        }

    if 'Bearer' in auth:
        auth = auth.replace('Bearer ', '', 1)

    token = jwt.decode(auth, jwt_key, algorithms=config["jwt_alg"])
    t = int(time.time())

    if token['iat'] + config['login_duration'] < t:
        c_auth_log.debug('User provided an expired token')
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
        c_auth_log.debug('User lacks permission for endpoint')
        return {
            "status": "fail",
            "fail_no": "3",
            "message": "You do not have high enough permissions to view this endpoint."
        }, 403, {"Content-Type": "application/json"}

    return True
