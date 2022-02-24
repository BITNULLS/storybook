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
    return "e"

@admin.route("/admin/book_manager")
def gen_admin_book_mananger():
    return "e"

@admin.route("/admin/edit_book")
def gen_admin_edit_book():
    return "e"

@admin.route("/admin/upload_book")
def gen_admin_upload_book():
    return "e"

@admin.route("/admin/study_manager")
def gen_admin_edit_book():
    return "e"
