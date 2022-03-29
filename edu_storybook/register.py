"""
register.py

This lets a user register for the website.
"""

import logging

from flask import request
from flask import Blueprint

from edu_storybook.templates import Templates
from edu_storybook.navbar import make_navbar
from edu_storybook.core.config import config

register = Blueprint('register', __name__)

log = logging.getLogger('ssg.register')
if config['production'] == False:
    log.setLevel(logging.DEBUG)

@register.route("/register")
def gen_register():
    '''
    Generate the register page.
    '''
    register_page = Templates._base.substitute(
        title = "Register an Account",
        description = "Make an account with our website",
        body = Templates.register.substitute(
             navbar = make_navbar( None )
        )
    )
    return register_page
