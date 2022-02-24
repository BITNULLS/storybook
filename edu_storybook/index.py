"""
Routes:
    /
    /api/
"""

from flask import request
from flask import make_response
from flask import Blueprint

from edu_storybook import TEMPLATES

homepage = Blueprint('homepage', __name__)

@homepage.route("/")
def gen_index():
    homepage = TEMPLATES["_base"].substitute(
        title = "EduStorybook Homepage",
        description = "A motivational storybook that helps students learn.",
        body = TEMPLATES["index"]
    )
    return homepage
