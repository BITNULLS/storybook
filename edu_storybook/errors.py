"""
errors.py
    Generates the error pages of the website.

Routes:
    /error/404
"""

from flask import request, Flask, render_template
from flask import make_response
from flask import Blueprint

from templates import TEMPLATES 

from navbar import make_navbar

errors = Blueprint('errors', __name__)

@errors.route("/error/404")
def page_not_found(e):
  return render_template('404.html'), 404

def create_app(config_filename):
    app = Flask(__name__)
    app.register_error_handler(404, page_not_found)
    return app

@errors.route("/error/401")
def page_not_found(e):
  return render_template('401.html'), 401


