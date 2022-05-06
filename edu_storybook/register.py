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
from edu_storybook.api.index import get_schools

register = Blueprint('register', __name__)

log = logging.getLogger('ssg.register')
if config['production'] == False:
    log.setLevel(logging.DEBUG)

@register.route("/register")
def gen_register():
    '''
    Generate the register page.
    '''
    school=""
    for s in get_schools(0)['schools']:
        school += Templates.school_card.substitute(
            school_name = s['SCHOOL_NAME'], 
            school_id = s['SCHOOL_ID']
        )

    register_page = Templates._base.substitute(
        title = "Register an Account",
        description = "Make an account with our website",
        body = Templates.register.substitute(
             navbar = make_navbar( None ), 
             schools = school
        )
    )
    return register_page
