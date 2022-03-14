"""
index.py
    Generates the homepage of the website.

Routes:
    /
"""

from flask import request
from flask import make_response
from flask import Blueprint

from templates import TEMPLATES

from navbar import make_navbar

homepage = Blueprint('homepage', __name__)

@homepage.route("/")
def gen_index():
    auth = None
    if 'Authorization' in request.cookies:
        auth = request.cookies['Authorization']

    the_homepage = TEMPLATES["_base"].substitute(
        title = "EduStorybook Homepage",
        description = "A motivational storybook that helps students learn.",
        body = TEMPLATES["index"].substitute(
            navbar = make_navbar( auth )
        )
    )
    return the_homepage
