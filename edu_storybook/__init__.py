"""
This script contains constants that all of the routes need.
"""

from string import Template

def load_template(filepath):
    """
    Read a file into a string.Template
    """
    t = None
    with open(filepath, 'r') as f:
        t = Template('\n'.join(f.readlines()))
    return t

# import all templates
TEMPLATES = {
    "admin": {
        "edit_book": load_template("../templates/admin/edit_book.html"),
        "view_page": load_template("../templates/admin/view_page.html")
    },
    "password": {
        "forgot": load_template("../templates/password/forgot.html"),
        "reset": load_template("../templates/password/reset.html")
    },
    "story_selection": {
        "book": load_template("../templates/story_selection/book.html"),
        "index": load_template("../templates/story_selection/index.html")
    },
    "storyboard": {
        "quiz": load_template("../templates/storyboard/quiz.html"),
        "viewer": load_template("../templates/storyboard/viewer.html")
    },
    "_base": load_template("../templates/_base.html"),
    "index": load_template("../templates/index.html"),
    "login": load_template("../templates/login.html"),
    "register": load_template("../templates/register.html")
}
