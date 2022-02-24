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
from flask import make_response

from .sensitive import jwt_key
from . import config
from .helper import label_results_from
from .email import send_email
from .reg_exps import *


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
