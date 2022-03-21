"""
admin.py
    Generate the pages for the "templates/admin/" templates.

Routes:
    /admin/
    /admin/book_manager
    /admin/edit_book
    /admin/study_manager
    /admin/upload_book
"""

import json
from flask import request
from flask import send_file
from flask import Blueprint
from api.index import get_book_info
from api.storyboard import storyboard_get_pagecount

from templates import TEMPLATES

from navbar import make_navbar

from api.admin import admin_get_books

admin = Blueprint('admin', __name__)



@admin.route("/admin/")
def gen_admin_index():

    auth = None
    if 'Authorization' in request.cookies:
        auth = request.cookies['Authorization']

    the_index_page = TEMPLATES["_base"].substitute(
        title = "Admin Homepage",
        description = "A motivational storybook that helps students learn.",
        body = TEMPLATES["admin"]["index"].substitute(
            navbar = make_navbar( auth )
        )
    )
    return the_index_page

@admin.route("/admin/book_manager")
def gen_admin_book_mananger():

    auth = None
    if 'Authorization' in request.cookies:
        auth = request.cookies['Authorization']

    book_manager_page = TEMPLATES["_base"].substitute(
        title = "Admin: Book Manager",
        description = "A motivational storybook that helps students learn.",
        body = TEMPLATES["admin"]["book_manager"].substitute(
            navbar = make_navbar( auth )
        )
    )
    return book_manager_page

@admin.route("/admin/edit_book")
def gen_admin_edit_book():

    auth = None
    if 'Authorization' in request.cookies:
        auth = request.cookies['Authorization']

    book_id = int(122)
    page_number = int(1)
    
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



    all_books = ""
    for b in admin_get_books(0)['books']:
        all_books += TEMPLATES['admin']['book'].substitute(
            book_title = b['BOOK_NAME'],
            book_description = b['DESCRIPTION'],
            book_id = b["BOOK_ID"]
        )      

    edit_book_page = TEMPLATES["_base"].substitute(
        title = "Admin: Edit Book",
        description = "A motivational storybook that helps students learn.",
        body = TEMPLATES["admin"]["edit_book"].substitute(
            navbar = make_navbar( auth ), 
            book = all_books, 

            current_page = "/api/storyboard/page/" + str(book_id) + "/" + str(page_number),
            id = str(book_id),
            prev_page_num = str(page_number - 1),
            next_page_num = str(page_number + 1),
            show_prev_link = prev_link_visibility,
            show_next_link = next_link_visibility

        )
    )
    return edit_book_page

@admin.route("/admin/upload_book")
def gen_admin_upload_book():

    auth = None
    if 'Authorization' in request.cookies:
        auth = request.cookies['Authorization']

    upload_book_page = TEMPLATES["_base"].substitute(
        title = "Admin: Upload Book",
        description = "A motivational storybook that helps students learn.",
        body = TEMPLATES["admin"]["upload_book"].substitute(
            navbar = make_navbar( auth )
        )
    )
    return upload_book_page

@admin.route("/admin/study_manager")
def gen_admin_study_manager():

    auth = None
    if 'Authorization' in request.cookies:
        auth = request.cookies['Authorization']

    study_manager_page = TEMPLATES["_base"].substitute(
        title = "Admin: Study Manager",
        description = "A motivational storybook that helps students learn.",
        body = TEMPLATES["admin"]["study_manager"].substitute(
            navbar = make_navbar( auth )
        )
    )
    return study_manager_page
