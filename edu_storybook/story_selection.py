"""
story_selection.py
    This will display all of the books that a user can look at.

Routes:
    /books
"""

import logging

from flask import request
from flask import Blueprint
from edu_storybook.api.index import get_users_books
from edu_storybook.core.config import config

from edu_storybook.templates import TEMPLATES

from edu_storybook.navbar import make_navbar

story_selection = Blueprint('story_selection', __name__)

log = logging.getLogger('ssg.story_selection')
if config['production'] == False:
    log.setLevel(logging.DEBUG)

@story_selection.route('/books')
def gen_books():    

    auth = None
    if 'Authorization' in request.cookies:
        auth = request.cookies['Authorization']
    
    all_books = ""
    for b in get_users_books()['books']:
        all_books += TEMPLATES['story_selection']['book'].substitute(
            book_title = b['BOOK_NAME'],
            book_description = b['DESCRIPTION'],
            book_id = b["BOOK_ID"], 
            book_cover = '/api/storyboard/cover/' + str(b['BOOK_ID']), 
            last_page=b['LAST_PAGE'], #if last_page is null then 0 
            book_url = '/storyboard/' + str(b['BOOK_ID'])+ '/' + str(b['LAST_PAGE'])
        )          
        
    story_selection_page = TEMPLATES["_base"].substitute(
        title = 'Book Selection',
        description = 'Select a book to read',
        body = TEMPLATES['story_selection']['index'].substitute(
            navbar = make_navbar( auth ),
            book= all_books 
        )
    )

    return story_selection_page
