"""
storyboard.py

This handles displaying the pages of the book, storing user actions, and
receiving quiz question responses from the user.
"""

import logging
import json

from flask import Blueprint
from flask import request
from flask import abort

from edu_storybook.templates import Templates
from edu_storybook.core.config import config
from edu_storybook.core.auth import validate_login
from edu_storybook.templates import Templates
from edu_storybook.core.config import config

from edu_storybook.api.storyboard import storyboard_get_pagecount
from edu_storybook.api.index import get_book_info

from edu_storybook.navbar import make_navbar

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
        vl = validate_login(
            auth,
            permission=0
        )
        if vl != True:
            log.debug(
                f'A non-admin user tried to access the /storyboard/{book_id_in}/{page_number_in} page.'
            )
            abort(403)
    else:
        log.debug(
            f'An unauthorized, logged out user tried to access the /storyboard/{book_id_in}/{page_number_in} page.'
        )
        abort(403)

    book_id = int(book_id_in)
    page_number = int(page_number_in)

    # Get book_info based on book_id from latest api endpoint /api/book/book_id
    book_info = json.loads(get_book_info(book_id))
    name = book_info['BOOK_NAME']
    page_count = book_info['PAGE_COUNT']

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
    storyboard_page = Templates._base.substitute(
        title = 'Storyboard Page',
        description = 'Make an account with our website',
        body = Templates.storyboard_viewer.substitute(
            navbar = make_navbar( auth ),
            id_of_book = book_id,
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

