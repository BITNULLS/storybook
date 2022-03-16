"""
login.py

Routes:

    /login
"""

from flask import request
from flask import Blueprint

from templates import TEMPLATES
from navbar import make_navbar

login = Blueprint('login', __name__)

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
