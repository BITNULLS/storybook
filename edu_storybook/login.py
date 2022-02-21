"""
Routes:
    /login
"""

from flask import request
from flask import Blueprint

login = Blueprint('login', __name__)

@login.route("/")
def ind():
    return "e"

