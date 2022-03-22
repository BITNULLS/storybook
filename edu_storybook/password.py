"""
password.py

Generates the webpages for the `/password/*` pages.
"""

import logging

from flask import request
from flask import Blueprint

from templates import TEMPLATES
from navbar import make_navbar
from core.config import config

password = Blueprint('password', __name__)

log = logging.getLogger('ssg.password')
if config['production'] == False:
    log.setLevel(logging.DEBUG)

@password.route("/password/forgot")
def gen_password_forgot():
    '''
    Generate the password forgot page.
    '''
    password_forgot_page = TEMPLATES["_base"].substitute(
        title = "Password Forgot",
        description = "Enter your email to request a password reset",
        body = TEMPLATES["password"]["forgot"].substitute(
            navbar = make_navbar( None )
        )
    )
    return password_forgot_page

@password.route("/password/reset")
def gen_password_reset():
    '''
    Generate the password reset page.
    '''
    password_reset_page = TEMPLATES["_base"].substitute(
        title = "Password Reset",
        description = "Reset your password",
        body = TEMPLATES["password"]["reset"].substitute(
            navbar = make_navbar( None )
        )
    )
    return password_reset_page
