"""
story_selection.py
    This will display all of the books that a user can look at.

Routes:
    /books
"""

from flask import request
from flask import Blueprint
from api.index import get_users_books

from templates import TEMPLATES

from navbar import make_navbar

story_selection = Blueprint('story_selection', __name__)

@story_selection.route('/books')
def gen_books():
    """
    all_books = ''
    user_books = get_users_books()

    for b in user_books:
        all_books += TEMPLATES['story_selection']['book'].substitute(
            book_title       = b['TITLE'],
            book_description = b['DESCRIPTION'],
            book_image       = '...', # TODO: figure out how to get
            book_link        = b['BOOK_ID']
        )
    """

    auth = None
    if 'Authorization' in request.cookies:
        auth = request.cookies['Authorization']

    story_selection_page = TEMPLATES["_base"].substitute(
        title = 'Book Selection',
        description = 'Select a book to read',
        body = TEMPLATES['story_selection']['index'].substitute(
            books='',
            navbar = make_navbar( auth )
        )
    )

    return story_selection_page
