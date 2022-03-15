"""
templates.py
    Initializes all of the templates used in the web app.
"""

from string import Template
import os


class EduTemplate(Template):
    delimiter = '~'
    idpattern = r'[a-z][_a-z0-9]*'


def load_template(filepath):
    """
    Read a file into a string.Template
    """
    t = None
    # TODO ASSERT FILEPATH IS LEGIT FILE
    #assert os.path.isfile(filepath), `Provided template '
    with open(filepath, 'r', encoding='utf-8') as f:
        t = EduTemplate('\n'.join(f.readlines()))
    return t

# import all templates
# TODO: I just realized too late that this could be type-safed by having this
# ... templates dict just be class Templates, with sublcass Admin, then subclass
# ... off that with BookManage. That way it's autocompleted and type safe.
# ... This is a future work kind of thing.
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
