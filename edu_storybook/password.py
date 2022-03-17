"""
password.py
    Generates the webpages for the "/password/" pages.

Routes:
    /password/forgot
    /password/reset
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
    password_reset_page = TEMPLATES["_base"].substitute(
        title = "Password Reset",
        description = "Reset your password",
        body = TEMPLATES["password"]["reset"].substitute(
            navbar = make_navbar( None )
        )
    )
    return password_reset_page
