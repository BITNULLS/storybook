"""
Routes:
    /
"""

from flask import request
from flask import Blueprint

homepage = Blueprint('homepage', __name__)

@homepage.route("/")
def index():
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