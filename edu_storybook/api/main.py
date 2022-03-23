"""
main.py
    Imports the routes of all other scripts in this module.
"""

from flask import Blueprint

import logging
logging.debug('Loading edu_storybook.api modules')

from edu_storybook.api import admin
from edu_storybook.api import index
from edu_storybook.api import password
from edu_storybook.api import quiz
from edu_storybook.api import storyboard
from edu_storybook.api import study

from edu_storybook.core.config import config

api = Blueprint('api', __name__)

api.register_blueprint(admin.a_admin)
api.register_blueprint(index.a_index)
api.register_blueprint(password.a_password)
api.register_blueprint(quiz.a_quiz)
api.register_blueprint(storyboard.a_storyboard)
api.register_blueprint(study.a_study)

a_main = logging.getLogger('api.main')
if config['production'] == False:
    a_main.setLevel(logging.DEBUG)
a_main.debug('Finished loading edu_storybook.api modules')
