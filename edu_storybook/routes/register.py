"""
Routes:
    ...
"""

from flask import request
from flask import Blueprint

register = Blueprint('register', __name__)

@register.route("/")
def ind():
    return "e"