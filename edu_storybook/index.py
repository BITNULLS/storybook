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

@homepage.route("/api/")
def api_index():
    # revalidate login
    if 'Authorization' in request.cookies:
        # check if a user has valid credentials
        auth = request.cookies.get('Authorization')
        vl = validate_login(
            auth,
            permission=0
        )
        if vl != True:
            return vl

        res = make_response({
            "status": "ok",
            "login": "reverified"
        })
        issue_auth_token(res, auth)
        return res
    return {
        "status": "ok"
    }

@homepage.route("/")
def index():
    homepage = TEMPLATES["_base"].substitute(
        title = "EduStorybook Homepage",
        description = "A motivational storybook that helps students learn.",
        body = TEMPLATES["index"]
    )
    return homepage