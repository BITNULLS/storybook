"""
register.py
    This lets a user register for the website.

Routes:


    /register
"""

from flask import request
from flask import Blueprint

from templates import TEMPLATES
from navbar import make_navbar

register = Blueprint('register', __name__)

@register.route("/register")
def gen_register():
    
    auth = None
    if 'Authorization' in request.cookies:
        auth = request.cookies['Authorization']

    register_page = TEMPLATES["_base"].substitute(
        title = "Register an Account",
        description = "Make an account with our website",
        body = TEMPLATES["register"].substitute(
             navbar = make_navbar( auth )
        )
    )
    return register_page
