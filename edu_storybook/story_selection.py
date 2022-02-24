"""
story_selection.py
    This will display all of the books that a user can look at.

Routes:
    /books
"""

from flask import request
from flask import Blueprint

from templates import TEMPLATES

story_selection = Blueprint('story_selection', __name__)

@story_selection.route("/books")
def gen_books():
    return "e"
