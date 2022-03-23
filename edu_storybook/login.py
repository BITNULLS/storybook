"""
login.py

Routes:

    /login
"""

from flask import request
from flask import Blueprint
import logging

from edu_storybook.templates import TEMPLATES
from edu_storybook.navbar import make_navbar
from edu_storybook.core.config import config

login = Blueprint('login', __name__)

log = logging.getLogger('ssg.login')
if config['production'] == False:
    log.setLevel(logging.DEBUG)

@login.route("/login")
def gen_login():
    
    auth = None
    if 'Authorization' in request.cookies:
        auth = request.cookies['Authorization']

    login_page = TEMPLATES["_base"].substitute(
        title = "Admin: Book Manager",
        description = "A motivational storybook that helps students learn.",
        body = TEMPLATES["login"].substitute(
            navbar = make_navbar( auth )
        )
    )
    return login_page

