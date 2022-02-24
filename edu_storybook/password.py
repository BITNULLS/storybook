"""
Routes:
    /password/forgot
    /password/reset
"""

from flask import request
from flask import Blueprint

from templates import TEMPLATES

password = Blueprint('password', __name__)

@password.route("/password/forgot")
def gen_password_forgot():
    return "e"

@password.route("/password/reset")
def gen_password_reset():
    return "e"
