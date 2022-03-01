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

@story_selection.route('/books')
def gen_books():
    """
    example:
    all_books = ""
    for b in book_query:
        books += TEMPLATES['story_selection']['book'].substitute(
            book_title=b['TITLE'],
            ...
        )
    story_selection_page = TEMPLATES["_base"].substitute(
        title = 'Book Selection',
        description = 'Select a book to read',
        body = TEMPLATES['story_selection']['index'].substitute(
            books=all_books
        )
    )
    """
    story_selection_page = TEMPLATES["_base"].substitute(
        title = 'Book Selection',
        description = 'Select a book to read',
        body = TEMPLATES['story_selection']['index'].substitute(
            books=''
        )
    )
    return story_selection_page
