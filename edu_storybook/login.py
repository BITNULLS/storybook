"""
login.py
    
Routes:
    /login
"""

from flask import request
from flask import Blueprint

from templates import TEMPLATES

login = Blueprint('login', __name__)

@login.route("/login/")
def gen_login():
    return "e"

