"""
storyboard.py
    This handles displaying the pages of the book, storing user actions, and
    receiving quiz question responses from the user.

Routes:
    /storyboard/page/<int:book_id_in>/<int:page_number_in>
"""

import logging

from flask import Blueprint

from templates import TEMPLATES
from core.config import config

from api.storyboard import storyboard_get_pagecount
from api.index import get_users_books

storyboard = Blueprint('storyboard', __name__)

log = logging.getLogger('ssg.storyboard')
if config['production'] == False:
    log.setLevel(logging.DEBUG)

@storyboard.route("/storyboard/<int:book_id_in>/<int:page_number_in>")
def gen_storyboard_page(book_id_in: int, page_number_in: int):
    
    book_id = int(book_id_in)
    page_number = int(page_number_in)
    
    pagecount = storyboard_get_pagecount(book_id)['pagecount'] # Get the number of pages based on book_id
    name = None
    
    # Get the name of the book based on 'book_id' to display it on Storyboard Viewer
    if name is None:
        for b in get_users_books()['books']:
            if b['BOOK_ID'] == book_id:
                name = b['BOOK_NAME']
                break
            
    
    # Display/Hide "Previous" link based on current page number
    if page_number == 1:
        prev_link_visibility = "display: none"
    else:
        prev_link_visibility = "display: block"
    
    # Display/Hide "Next" link based on current page number
    if page_number == pagecount:
        next_link_visibility = "display: none"
    else:
        next_link_visibility = "display: block"

    storyboard_page = TEMPLATES['_base'].substitute(
        title = 'Storyboard Page',
        description = 'Make an account with our website',
        body = TEMPLATES['storyboard']['viewer'].substitute(
            book_name = name,
            current_page = "/api/storyboard/page/" + str(book_id) + "/" + str(page_number),
            id = str(book_id),
            prev_page_num = str(page_number - 1),
            next_page_num = str(page_number + 1),
            showPrevLink = prev_link_visibility,
            showNextLink = next_link_visibility
        )
    )
    return storyboard_page

