"""
templates.py

Initializes all of the templates used in the web app.

**NOTE**: It is strongly preferred that you use the Template class for referring
to templates. It is safer since it is type-hinted and checked at compile time
rather runtime.
"""

from json import load
import logging
from edu_storybook.core.config import Config
from edu_storybook.core.filepath import fix_filepath

from string import Template
import os

log = logging.getLogger('templates')
if Config.production == False:
    log.setLevel(logging.DEBUG)


class EduTemplate(Template):
    '''
    Update regular `string.Template` to use a new delimiter, `~`, and make the
    `idpattern` more narrow (`a-z`, `_`, and `0-9`).
    '''
    delimiter = '¶'
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
    filepath = fix_filepath(__file__, filepath)
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
        "upload_book": load_template("templates/admin/upload_book.html"), 
        "book": load_template("templates/admin/book.html"), 
        "book_card": load_template("templates/admin/book_card.html"),
        "study_list": load_template("templates/admin/study_list.html"), 
        "add_study": load_template("templates/admin/add_to_study.html"), 
        "user_list": load_template("templates/admin/user_list.html"),
        "add_book": load_template("templates/admin/add_to_book.html"),
        "add_user": load_template("templates/admin/add_to_user.html"),
        "school_options": load_template("templates/admin/school_id_option.html")
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
        "quiz": {
            "fr": load_template("templates/storyboard/quiz_fr.html"),
            "mc_item": load_template("templates/storyboard/quiz_mc_item.html"),
            "mc": load_template("templates/storyboard/quiz_mc.html"),
            "feedback": load_template("templates/storyboard/quiz_feedback.html")
        },
        "viewer": load_template("templates/storyboard/viewer.html")
    },
    "errors": {
        "400": load_template("templates/errors/400.html"),
        "401": load_template("templates/errors/401.html"),
        "403": load_template("templates/errors/403.html"),
        "404": load_template("templates/errors/404.html"),
        "405": load_template("templates/errors/405.html"),
        "500": load_template("templates/errors/500.html"),
        "502": load_template("templates/errors/502.html")
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

    admin_book: Template = TEMPLATES['admin']['book']
    '''
    Admin Book Index template.
    '''

    admin_book_card: Template = TEMPLATES['admin']['book_card']
    '''
    Admin Book Card template.
    '''

    admin_book_manager: Template = TEMPLATES['admin']['book_manager']
    '''
    Admin Book Manager template.
    '''

    admin_edit_book: Template = TEMPLATES['admin']['edit_book']
    '''
    Admin Edit Book template.
    '''

    admin_index: Template = TEMPLATES['admin']['index']
    '''
    Admin Index template.
    '''

    admin_study_mananger: Template = TEMPLATES['admin']['study_manager']
    '''
    Admin Study Manager template.
    '''

    admin_study_list: Template = TEMPLATES['admin']['study_list']

    admin_add_study: Template = TEMPLATES['admin']['add_study']

    admin_add_book: Template = TEMPLATES['admin']['add_book']

    admin_add_user: Template = TEMPLATES['admin']['add_user']

    admin_user_list: Template = TEMPLATES['admin']['user_list']

    admin_school_list: Template = TEMPLATES['admin']['school_options']

    admin_upload_book: Template = TEMPLATES['admin']['upload_book']
    '''
    Admin Upload Book template.
    '''

    navbar_logged_admin: Template = TEMPLATES['navbar']['logged_admin']
    '''
    Navbar Logged In Admin template.
    '''

    navbar_logged_out: Template = TEMPLATES['navbar']['logged_out']
    '''
    Navbar Logged Out template.
    '''

    navbar_logged_user: Template = TEMPLATES['navbar']['logged_user']
    '''
    Navbar Logged In User template.
    '''

    password_forgot: Template = TEMPLATES['password']['forgot']
    '''
    Password Forgot template.
    '''

    password_reset: Template = TEMPLATES['password']['reset']
    '''
    Password Reset template.
    '''

    story_selection_book: Template = TEMPLATES['story_selection']['book']
    '''
    Book template that appears in the Story Selection Index template.
    '''

    story_selection_index: Template = TEMPLATES['story_selection']['index']
    '''
    Story Selection template, that contains multiple `story_selection_book`
    templates (for each book).
    '''

    storyboard_quiz_fr: Template = TEMPLATES['storyboard']['quiz']['fr']
    '''
    Storyboard Quiz Free Response (FR) template.
    '''

    storyboard_quiz_mc_item: Template = TEMPLATES['storyboard']['quiz']['mc_item']
    '''
    Storyboard Quiz Multiple Choice (MC) item template, which appears in the
    Storyboard Quiz MC template. This is the individual MC answer, of which,
    likely multiple will appear for a multiple choice question.
    '''

    storyboard_quiz_mc: Template = TEMPLATES['storyboard']['quiz']['mc']
    '''
    Storyboard Quiz Multiple Choice (MC) template.
    '''
    
    storyboard_quiz_feedback: Template = TEMPLATES['storyboard']['quiz']['feedback']
    '''
    Storyboard Quiz Multiple Choice (MC) feedback template.
    '''

    storyboard_viewer: Template = TEMPLATES['storyboard']['viewer']
    '''
    Storyboard Viewer template.
    '''

    _base: Template = TEMPLATES['_base']
    '''
    The base template that every other template should be baked into.
    '''

    index: Template = TEMPLATES['index']
    '''
    Index template. The homepage of the website.
    '''

    login: Template = TEMPLATES['login']
    '''
    Login template.
    '''

    register: Template = TEMPLATES['register']
    '''
    Register template.
    '''
