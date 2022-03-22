"""
index.py

Generates the homepage of the website.
"""

from flask import request
from flask import make_response
from flask import Blueprint
import logging

from templates import Templates

from navbar import make_navbar
from core.config import config

homepage = Blueprint('homepage', __name__)

log = logging.getLogger('ssg.index')
if config['production'] == False:
    log.setLevel(logging.DEBUG)

@homepage.route("/")
def gen_index():
    '''
    Generates the homepage.
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
