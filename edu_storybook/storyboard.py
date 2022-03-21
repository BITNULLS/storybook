"""
storyboard.py

This handles displaying the pages of the book, storing user actions, and
receiving quiz question responses from the user.
"""

import logging
import json

from flask import Blueprint
from flask import request

from templates import TEMPLATES
from core.config import config

from api.storyboard import storyboard_get_pagecount
from api.index import get_book_info

from navbar import make_navbar

storyboard = Blueprint('storyboard', __name__)

log = logging.getLogger('ssg.storyboard')
if config['production'] == False:
    log.setLevel(logging.DEBUG)

@storyboard.route("/storyboard/<int:book_id_in>/<int:page_number_in>")
def gen_storyboard_page(book_id_in: int, page_number_in: int):
    '''
    Generate the storyboard viewer page.
    '''
    auth = None
    if 'Authorization' in request.cookies:
        auth = request.cookies['Authorization']
    
    book_id = int(book_id_in)
    page_number = int(page_number_in)
    
    page_count = storyboard_get_pagecount(book_id)['pagecount'] # Get the number of pages based on book_id
    
    # Get book_info based on book_id from latest api endpoint /api/book/book_id
    book_info = json.loads(get_book_info(book_id))
    name = book_info['BOOK_NAME']
            
    # Display/Hide "Previous" link based on current page number
    if page_number == 1:
        prev_link_visibility = "display: none"
    else:
        prev_link_visibility = "display: block"
    
    # Display/Hide "Next" link based on current page number
    if page_number == page_count:
        next_link_visibility = "display: none"
    else:
        next_link_visibility = "display: block"

    # Generate Storyboard Viewer page
    storyboard_page = TEMPLATES['_base'].substitute(
        title = 'Storyboard Page',
        description = 'Make an account with our website',
        body = TEMPLATES['storyboard']['viewer'].substitute(
            navbar = make_navbar( auth ),
            book_name = name,
            current_page = "/api/storyboard/page/" + str(book_id) + "/" + str(page_number),
            id = str(book_id),
            prev_page_num = str(page_number - 1),
            next_page_num = str(page_number + 1),
            show_prev_link = prev_link_visibility,
            show_next_link = next_link_visibility
        )
    )
    return storyboard_page

