"""
login.py

Routes:

    /login
    
"""

from flask import request
from flask import Blueprint

from templates import TEMPLATES

login = Blueprint('login', __name__)

@login.route("/login")
def gen_login():
    login_page = TEMPLATES["_base"].substitute(
        title = "Admin: Book Manager",
        description = "A motivational storybook that helps students learn.",
        body = TEMPLATES["login"].substitute()
    )
    return login_page

