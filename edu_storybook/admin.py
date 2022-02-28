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

from templates import TEMPLATES

admin = Blueprint('admin', __name__)

@admin.route("/admin/")
def gen_admin_index():
    the_index_page = TEMPLATES["_base"].substitute(
        title = "Admin Homepage",
        description = "A motivational storybook that helps students learn.",
        body = TEMPLATES["admin"]["index"].substitute()
    )
    return the_index_page

@admin.route("/admin/book_manager")
def gen_admin_book_mananger():
    book_manager_page = TEMPLATES["_base"].substitute(
        title = "Admin: Book Manager",
        description = "A motivational storybook that helps students learn.",
        body = TEMPLATES["admin"]["book_manager"].substitute()
    )
    return book_manager_page

@admin.route("/admin/edit_book")
def gen_admin_edit_book():
    edit_book_page = TEMPLATES["_base"].substitute(
        title = "Admin: Edit Book",
        description = "A motivational storybook that helps students learn.",
        body = TEMPLATES["admin"]["edit_book"].substitute()
    )
    return edit_book_page

@admin.route("/admin/upload_book")
def gen_admin_upload_book():
    upload_book_page = TEMPLATES["_base"].substitute(
        title = "Admin: Upload Book",
        description = "A motivational storybook that helps students learn.",
        body = TEMPLATES["admin"]["upload_book"].substitute()
    )
    return upload_book_page

@admin.route("/admin/study_manager")
def gen_admin_study_manager():
    study_manager_page = TEMPLATES["_base"].substitute(
        title = "Admin: Study Manager",
        description = "A motivational storybook that helps students learn.",
        body = TEMPLATES["admin"]["study_manager"].substitute()
    )
    return study_manager_page
