"""
errors.py
    Generates the error pages of the website.

Routes:
    /error/401
    /error/403
    /error/404
    /error/405
    /error/500
    /error/502
"""

from flask import request, Flask, render_template
from flask import make_response
from flask import Blueprint

from templates import TEMPLATES 

from navbar import make_navbar

errors = Blueprint('errors', __name__)

@errors.route("/error/400")
def page_not_found_400():
  page_400 = TEMPLATES["_base"].substitute(
    title = "400 Error",
    description = "",
    body = TEMPLATES['errors']['400'].substitute(
     navbar = make_navbar( None )
    )
  )
  return page_400

@errors.route("/error/401")
def page_not_found_401():
  page_401 = TEMPLATES["_base"].substitute(
    title = "401 Error",
    description = "",
    body = TEMPLATES['errors']['401'].substitute(
     navbar = make_navbar( None )
    )
  )
  return page_401

@errors.route("/error/403")
def page_not_found_403():
  page_403 = TEMPLATES["_base"].substitute(
    title = "403 Error",
    description = "",
    body = TEMPLATES['errors']['403'].substitute(
     navbar = make_navbar( None )
    )
  )
  return page_403

@errors.route("/error/404")
def page_not_found_404():
  page_404 = TEMPLATES["_base"].substitute(
    title = "404 Error",
    description = "",
    body = TEMPLATES['errors']['404'].substitute(
     navbar = make_navbar( None )
    )
  )
  return page_404

@errors.route("/error/405")
def page_not_found_405():
  page_405 = TEMPLATES["_base"].substitute(
    title = "405 Error",
    description = "",
    body = TEMPLATES['errors']['405'].substitute(
     navbar = make_navbar( None )
    )
  )
  return page_405

@errors.route("/error/500")
def page_not_found_500():
  page_500= TEMPLATES["_base"].substitute(
    title = "500 Error",
    description = "",
    body = TEMPLATES['errors']['500'].substitute(
     navbar = make_navbar( None )
    )
  )
  return page_500

@errors.route("/error/502")
def page_not_found_502():
  page_502 = TEMPLATES["_base"].substitute(
    title = "502 Error",
    description = "",
    body = TEMPLATES['errors']['502'].substitute(
     navbar = make_navbar( None )
    )
  )
  return page_502

