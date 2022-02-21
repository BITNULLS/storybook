"""
Routes:
    ...
"""

from flask import request
from flask import Blueprint

story_selection = Blueprint('story_selection', __name__)

@story_selection.route("/")
def ind():
    return "e"
