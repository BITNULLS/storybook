"""
story_selection.py

This will display all of the books that a user can look at.
"""

import logging

from flask import request
from flask import Blueprint
from flask import abort

from edu_storybook.api.index import get_users_books
from edu_storybook.core import auth
from edu_storybook.core.config import config
from edu_storybook.core.auth import validate_login
from edu_storybook.templates import Templates
from edu_storybook.navbar import make_navbar

story_selection = Blueprint('story_selection', __name__)

log = logging.getLogger('ssg.story_selection')
if config['production'] == False:
    log.setLevel(logging.DEBUG)


@story_selection.route('/books')
def gen_books():
    '''
    Generate the story selection (books) page.
    
    When registering as a user, the register page redirects to 
    story Selection with admin navbar (not user).
    an issue with make_navbar(auth) may arise where auth may be incorrectly setup
    '''
    auth = None
    if 'Authorization' in request.cookies:
        auth = request.cookies['Authorization']
    else:
        abort(403, description="You are not logged in.")

    vl = validate_login(
        auth,
        permission=0
    )

    if vl != True:
        log.debug('A non-admin user tried to access the /books page.')
        abort(403)

    all_books = ""
    for b in get_users_books()['books']:
        all_books += Templates.story_selection_book.substitute(
        book_title=b['BOOK_NAME'],
        book_description=b['DESCRIPTION'],
        book_id=b["BOOK_ID"],
        book_cover='/api/storyboard/cover/' + str(b['BOOK_ID']),
        last_page=b['LAST_PAGE'],  # if last_page is null then 0
        book_url='/storyboard/' + str(b['BOOK_ID']) + '/' + str(b['LAST_PAGE'])
    )

    story_selection_page = Templates._base.substitute(
        title='Book Selection',
        description='Select a book to read',
        body=Templates.story_selection_index.substitute(
            navbar=make_navbar(auth),
            book=all_books
        )
    )
    return story_selection_page
