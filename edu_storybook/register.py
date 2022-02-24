"""
register.py
    This lets a user register for the website.

Routes:
    /register
"""

from flask import request
from flask import Blueprint

from templates import TEMPLATES

register = Blueprint('register', __name__)

@register.route("/register")
def gen_register():
    return "e"
