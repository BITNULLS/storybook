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

from flask import request
from flask import send_file
from flask import Blueprint
from flask import abort
from templates import TEMPLATES

from navbar import make_navbar

admin = Blueprint('admin', __name__)

@admin.route("/admin/")
def gen_admin_index():

    auth = None
    if 'Authorization' in request.cookies:
        auth = request.cookies['Authorization']
    else:
        abort(401, description="You are not logged in.")

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
    else:
        abort(401, description="You are not logged in.")

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
    else:
        abort(401, description="You are not logged in.")

    edit_book_page = TEMPLATES["_base"].substitute(
        title = "Admin: Edit Book",
        description = "A motivational storybook that helps students learn.",
        body = TEMPLATES["admin"]["edit_book"].substitute(
            navbar = make_navbar( auth )
        )
    )
    return edit_book_page

@admin.route("/admin/upload_book")
def gen_admin_upload_book():

    auth = None
    if 'Authorization' in request.cookies:
        auth = request.cookies['Authorization']
    else:
        abort(401, description="You are not logged in.")

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
    else:
        abort(401, description="You are not logged in.")

    study_manager_page = TEMPLATES["_base"].substitute(
        title = "Admin: Study Manager",
        description = "A motivational storybook that helps students learn.",
        body = TEMPLATES["admin"]["study_manager"].substitute(
            navbar = make_navbar( auth )
        )
    )
    return study_manager_page
