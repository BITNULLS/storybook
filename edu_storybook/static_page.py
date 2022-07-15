"""
static_page.py

Generates the static pages of the site.
"""

from flask import request
from flask import make_response
from flask import Blueprint
import logging

from edu_storybook.templates import Templates
from edu_storybook.navbar import make_navbar
from edu_storybook.core.config import config

homepage = Blueprint('homepage', __name__)

log = logging.getLogger('ssg.static_page')
if config['production'] == False:
    log.setLevel(logging.DEBUG)

@homepage.route("/static_page/<str:page_name_in>")
def gen_static_page(page_name_in: str):
    '''
    Generates a static page.
    '''
    auth = None
    if 'Authorization' in request.cookies:
        auth = request.cookies['Authorization']

    the_homepage = Templates._base.substitute(
        title = "EduStorybook Homepage",
        description = "A motivational storybook that helps students learn.",
        body = Templates.index.substitute(
            navbar = make_navbar( auth )
        )
    )
    return the_homepage
