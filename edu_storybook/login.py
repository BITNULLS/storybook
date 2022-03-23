"""
login.py

Generates the login page.
"""

from flask import request
from flask import Blueprint
import logging

from edu_storybook.templates import Templates
from edu_storybook.navbar import make_navbar
from edu_storybook.core.config import config

login = Blueprint('login', __name__)

log = logging.getLogger('ssg.login')
if config['production'] == False:
    log.setLevel(logging.DEBUG)

@login.route("/login")
def gen_login():
    '''
    Generates the login page.
    '''
    auth = None
    if 'Authorization' in request.cookies:
        auth = request.cookies['Authorization']

    login_page = Templates._base.substitute(
        title = "Admin: Book Manager",
        description = "A motivational storybook that helps students learn.",
        body = Templates.login.substitute(
            navbar = make_navbar( auth )
        )
    )
    return login_page

