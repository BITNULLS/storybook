"""
storyboard.py
    This handles displaying the pages of the book, storing user actions, and
    receiving quiz question responses from the user.

Routes:
    /storyboard/page/<int:book_id_in>/<int:page_number_in>
"""

import logging

from pydoc import pager
from flask import request
from flask import Blueprint

from templates import TEMPLATES
from core.config import config

storyboard = Blueprint('storyboard', __name__)

log = logging.getLogger('ssg.storyboard')
if config['production'] == False:
    log.setLevel(logging.DEBUG)

@storyboard.route("/storyboard/<int:book_id_in>/<int:page_number_in>")
def gen_storyboard_page(book_id_in: int, page_number_in: int):
    storyboard_page = TEMPLATES['_base'].substitute(
        title = 'Storyboard Page',
        description = 'Make an account with our website',
        body = TEMPLATES['story_selection']['index'].substitute()
    )
    return storyboard_page
