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
from api.storyboard import storyboard_get_page
from templates import TEMPLATES

storyboard = Blueprint('storyboard', __name__)

@storyboard.route("/storyboard/page/<int:book_id_in>/<int:page_number_in>")
def gen_storyboard_page(book_id_in, page_number_in):
    #slide = storyboard_get_page(book_id_in, page_number_in)
    ''' 
        need to swithc storyboard index in templates to viewer or quiz ;
        so check if type of slide is a dictionary = quiz question 
        if type is flask.response = image of the book
    '''
    storyboard_page = TEMPLATES['_base'].substitute(
        title = 'Storyboard Page',
        description = 'Make an account with our website',
        body = TEMPLATES['storyboard']['viewer'].substitute()#book_image=slide)
    )
    return storyboard_page
