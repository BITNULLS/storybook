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
from templates import TEMPLATES
from templates import Templates

from navbar import make_navbar

from api.admin import admin_get_books

from flask import request
from flask import Blueprint

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

    all_books = ""
    for b in admin_get_books(0)['books']:
        all_books += Templates.admin_book.substitute(
            book_title = b['BOOK_NAME'],
            book_description = b['DESCRIPTION'],
            book_id = b["BOOK_ID"],
            book_pages = b["PAGE_COUNT"]
        )      

    edit_book_page = Templates._base.substitute(
        title = "Admin: Edit Book",
        description = "A motivational storybook that helps students learn.",
        body = Templates.admin_edit_book.substitute(
            navbar = make_navbar( auth ), 
            book = all_books, 
            
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
