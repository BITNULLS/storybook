"""
templates.py
    Initializes all of the templates used in the web app.
"""

import logging
from core.config import config

from string import Template
import os

log = logging.getLogger('templates')
if config['production'] == False:
    log.setLevel(logging.DEBUG)


class EduTemplate(Template):
    '''
    Update regular `string.Template` to use a new delimiter, `~`, and make the
    `idpattern` more narrow (`a-z`, `_`, and `0-9`).
    '''
    delimiter = '~'
    idpattern = r'[a-z][_a-z0-9]*'


def load_template(filepath: str) -> EduTemplate:
    """
    Read a file into a `string.Template` Python built-in class.

    Args:
     - filepath: The path to a template

    Returns: A loaded template.
    """
    t = None
    # TODO ASSERT FILEPATH IS LEGIT FILE
    #assert os.path.isfile(filepath), `Provided template '
    with open(filepath, 'r', encoding='utf-8') as f:
        t = EduTemplate('\n'.join(f.readlines()))
    return t

# import all templates
TEMPLATES = {
    "admin": {
        "book_manager": load_template("templates/admin/book_manager.html"),
        "edit_book": load_template("templates/admin/edit_book.html"),
        "index": load_template("templates/admin/index.html"),
        "study_manager": load_template("templates/admin/study_manager.html"),
        "upload_book": load_template("templates/admin/upload_book.html")
    },
    "navbar": {
        "logged_admin": load_template("templates/navbar/logged_admin.html"),
        "logged_out": load_template("templates/navbar/logged_out.html"),
        "logged_user": load_template("templates/navbar/logged_user.html")
    },
    "password": {
        "forgot": load_template("templates/password/forgot.html"),
        "reset": load_template("templates/password/reset.html")
    },
    "story_selection": {
        "book": load_template("templates/story_selection/book.html"),
        "index": load_template("templates/story_selection/index.html")
    },
    "storyboard": {
        "quiz": load_template("templates/storyboard/quiz.html"),
        "viewer": load_template("templates/storyboard/viewer.html")
    },
    "_base": load_template("templates/_base.html"),
    "index": load_template("templates/index.html"),
    "login": load_template("templates/login.html"),
    "register": load_template("templates/register.html")
}

class Templates:
    '''
    This Templates class just holds references to `TEMPLATES` where the
    templates are actually loaded and initialized.

    This class will help type safety, and make it easier for our contributors.
    '''
    admin_book_manager: Template = TEMPLATES['admin']['book_manager']
    admin_edit_book: Template = TEMPLATES['admin']['edit_book']
    admin_index: Template = TEMPLATES['admin']['index']
    admin_study_mananger: Template = TEMPLATES['admin']['study_manager']
    admin_upload_book: Template = TEMPLATES['admin']['upload_book']
    navbar_logged_admin: Template = TEMPLATES['navbar']['logged_admin']
    navbar_logged_out: Template = TEMPLATES['navbar']['logged_out']
    navbar_logged_user: Template = TEMPLATES['navbar']['logged_user']
    password_forgot: Template = TEMPLATES['password']['forgot']
    password_reset: Template = TEMPLATES['password']['reset']
    story_selection_book: Template = TEMPLATES['story_selection']['book']
    story_selection_index: Template = TEMPLATES['story_selection']['index']
    storyboard_quiz: Template = TEMPLATES['storyboard']['quiz']
    storyboard_viewer: Template = TEMPLATES['storyboard']['viewer']
    _base: Template = TEMPLATES['_base']
    index: Template = TEMPLATES['index']
    login: Template = TEMPLATES['login']
    register: Template = TEMPLATES['register']
