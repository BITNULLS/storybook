"""
storyboard.py
    This handles displaying the pages of the book, storing user actions, and
    receiving quiz question responses from the user.

Routes:
    /storyboard/page/<int:book_id_in>/<int:page_number_in>
"""

from pydoc import pager
from flask import request
from flask import Blueprint

from templates import TEMPLATES

storyboard = Blueprint('storyboard', __name__)

@storyboard.route("/storyboard/<int:book_id_in>/<int:page_number_in>")
def gen_storyboard_page():
    return "e"
