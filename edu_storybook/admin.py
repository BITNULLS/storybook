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
from edu_storybook.api.study import get_studies
from edu_storybook.core import auth

import logging
from edu_storybook.core.auth import validate_login

from edu_storybook.templates import Templates
from edu_storybook.core.config import config
from edu_storybook.navbar import make_navbar

from edu_storybook.api.admin import admin_get_books, admin_get_users

from flask import request
from flask import Blueprint

admin = Blueprint('admin', __name__)

log = logging.getLogger('ssg.admin')
if config['production'] == False:
    log.setLevel(logging.DEBUG)


@admin.route("/admin/")
def gen_admin_index():
    """
    Generate the `/admin/` index page.
    """

    auth = None
    if 'Authorization' in request.cookies:
        auth = request.cookies['Authorization']
    else:
        log.debug('An unauthorized, logged out user tried to access the ' +\
            '/admin/ page.')
        abort(401, description="You are not logged in.")

    vl = validate_login(
            auth,
            permission=1
        )
    if vl != True:
        log.debug('A non-admin user tried to access the /admin/ page.')
        abort(403)

    the_index_page = Templates._base.substitute(
        title = "Admin Homepage",
        description = "A motivational storybook that helps students learn.",
        body = Templates.admin_index.substitute(
            navbar = make_navbar( auth )
        )
    )
    return the_index_page

@admin.route("/admin/book_manager")
def gen_admin_book_mananger():
    """
    Generate the `/admin/book_manager` page.
    """

    auth = None
    if 'Authorization' in request.cookies:
        auth = request.cookies['Authorization']
    else:
        log.debug(
            'An unauthorized, logged out user tried to access the ' +\
                '/admin/book_manager page.'
        )
        abort(401, description="You are not logged in.")

    vl = validate_login(
        auth,
        permission=1
    )
    if vl != True:
        log.debug(
            'A non-admin user tried to access the /admin/book_manager page.'
            )
        abort(403)
    all_books = ""
    for b in admin_get_books(0)['books']:
        all_books += Templates.admin_book_card.substitute(
            book_title = b['BOOK_NAME'],
            book_description = b['DESCRIPTION'],
            book_id = b["BOOK_ID"],
            book_pages = b['PAGE_COUNT'],
            book_cover = '/api/storyboard/cover/' + str(b['BOOK_ID']),
            book_study = b['STUDY_ID']
        )
    addStudy = ""
    for s in get_studies(0)['studies']:
        addStudy += Templates.admin_add_study.substitute(
            study_id = s['STUDY_ID'],
            study_name = s['STUDY_NAME'],
            school_name = s['SCHOOL_NAME']
        )

    book_manager_page = Templates._base.substitute(
        title = "Admin: Book Manager",
        description = "A motivational storybook that helps students learn.",
        body = Templates.admin_book_manager.substitute(
            navbar = make_navbar( auth ),
            book = all_books,
            addStudy= addStudy
        )
    )
    return book_manager_page


@admin.route("/admin/edit_book")
def gen_admin_edit_book():
    """
    Generate the `/admin/edit_book` page.
    """

    auth = None
    if 'Authorization' in request.cookies:
        auth = request.cookies['Authorization']
    else:
        log.debug(
            'An unauthorized, logged out user tried to access the ' +\
                '/admin/edit_book page.'
        )
        abort(401, description="You are not logged in.")

    vl = validate_login(
        auth,
        permission=1
        )
    if vl != True:
        log.debug(
            'A non-admin user tried to access the /admin/edit_book page.'
        )
        abort(403)

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
            book = all_books
        )
    )
    return edit_book_page


@admin.route("/admin/upload_book")
def gen_admin_upload_book():
    """
    Generate the `/admin/upload_book` page.
    """

    auth = None
    if 'Authorization' in request.cookies:
        auth = request.cookies['Authorization']
    else:
        log.debug(
            'An unauthorized, logged out user tried to access the ' +\
                '/admin/upload_book page.'
        )
        abort(401, description="You are not logged in.")

    vl = validate_login(
        auth,
        permission=1
    )

    if vl != True:
        log.debug(
            'A non-admin user tried to access the /admin/upload_book page.'
            )
        abort(403)

    addStudy = ""
    for s in get_studies(0)['studies']:
        addStudy += Templates.admin_add_study.substitute(
            study_id = s['STUDY_ID'],
            study_name = s['STUDY_NAME'],
            school_name = s['SCHOOL_NAME']
        )

    upload_book_page = Templates._base.substitute(
        title = "Admin: Upload Book",
        description = "A motivational storybook that helps students learn.",
        body = Templates.admin_upload_book.substitute(
            navbar = make_navbar( auth ),
            add_study = addStudy
        )
    )
    return upload_book_page


@admin.route("/admin/study_manager")
def gen_admin_study_manager():
    """
    Generate the `/admin/study_manager` page.
    """

    auth = None
    if 'Authorization' in request.cookies:
        auth = request.cookies['Authorization']
    else:
        log.debug(
            'An unauthorized, logged out user tried to access the ' +\
                '/admin/study_manager page.'
        )
        abort(401, description="You are not logged in.")

    vl = validate_login(
        auth,
        permission=1
    )

    if vl != True:
        log.debug(
            'A non-admin user tried to access the /admin/study_manager page.'
            )
        abort(403)
    studies = ""
    addStudy = ""
    for s in get_studies(0)['studies']:
        studies += Templates.admin_study_list.substitute(
            study_id = s['STUDY_ID'],
            study_name = s['STUDY_NAME'],
            school_name = s['SCHOOL_NAME']
        )
        addStudy += Templates.admin_add_study.substitute(
            study_id = s['STUDY_ID'],
            study_name = s['STUDY_NAME'],
            school_name = s['SCHOOL_NAME']
        )
    users =""
    addUsers = ""
    for u in admin_get_users(0)['users']:
        addUsers += Templates.admin_add_user.substitute(
            user_email = u['EMAIL'],
            user_name = u['FIRST_NAME'],
            user_last = u['LAST_NAME'],
            user_id = u['USER_ID']
        )
        users += Templates.admin_user_list.substitute(
            user_email = u['EMAIL'],
            user_name = u['FIRST_NAME'],
            user_last = u['LAST_NAME'],
            user_id = u['USER_ID']
        )

    addBooks = ""
    for b in admin_get_books(0)['books']:
        addBooks += Templates.admin_add_book.substitute(
            book_title = b['BOOK_NAME'],
            book_description = b['DESCRIPTION'],
            book_id = b["BOOK_ID"],
            book_pages = b['PAGE_COUNT']
            #book_study = b['STUDY_ID']
        )
    study_manager_page = Templates._base.substitute(
        title = "Admin: Study Manager",
        description = "A motivational storybook that helps students learn.",
        body = Templates.admin_study_mananger.substitute(
            navbar = make_navbar( auth ),
            study_list = studies,
            add_study = addStudy,
            user_list = users,
            add_user= addUsers,
            add_book = addBooks
        )
    )
    return study_manager_page
