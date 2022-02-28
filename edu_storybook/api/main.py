"""
main.py
    Imports the routes of all other scripts in this module.
"""

from flask import Blueprint

from . import admin
from . import index
from . import password
from . import quiz
from . import storyboard

api = Blueprint('api', __name__)

api.register_blueprint(admin.a_admin)
api.register_blueprint(index.a_index)
api.register_blueprint(password.a_password)
api.register_blueprint(quiz.a_quiz)
api.register_blueprint(storyboard.a_storyboard)
