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

    auth = None
    if 'Authorization' in request.cookies:
        auth = request.cookies['Authorization']
    
    all_books = ""
    for b in get_users_books()['books']:
        all_books += TEMPLATES['story_selection']['book'].substitute(
            book_title = b['BOOK_NAME'],
            book_description = b['DESCRIPTION']
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
