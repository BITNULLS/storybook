"""
app.py
    Main launch point for our web server.
"""

from distutils.log import error
from flask import Flask
from api import main 
import admin
import index
import login
import password
import register    
import story_selection 
import storyboard 
from templates import TEMPLATES
from navbar import make_navbar 
import errors
   
 
app = Flask(__name__, static_url_path="/static/", static_folder="static")

app.register_blueprint(main.api) 
app.register_blueprint(admin.admin)
app.register_blueprint(index.homepage)
app.register_blueprint(login.login)
app.register_blueprint(password.password)
app.register_blueprint(register.register)
app.register_blueprint(story_selection.story_selection)
app.register_blueprint(storyboard.storyboard)

@app.errorhandler(400)
def page_not_found_400(e):
  page_400 = TEMPLATES["_base"].substitute(
    title = "400 Error",
    description = str(e),
    body = TEMPLATES['errors']['400'].substitute(
     navbar = make_navbar( None )
    )
  )
  return page_400

@app.errorhandler(401)
def page_not_found_401(e):
  page_401 = TEMPLATES["_base"].substitute(
    title = "401 Error",
    description = str(e),
    body = TEMPLATES['errors']['401'].substitute(
     navbar = make_navbar( None )
    )
  )
  return page_401

@app.errorhandler(403)
def page_not_found_403(e):
  page_403 = TEMPLATES["_base"].substitute(
    title = "403 Error",
    description = str(e),
    body = TEMPLATES['errors']['403'].substitute(
     navbar = make_navbar( None )
    )
  )
  return page_403

@app.errorhandler(404)
def page_not_found_404(e):
  page_404 = TEMPLATES["_base"].substitute(
    title = "404 Error",
    description = str(e),
    body = TEMPLATES['errors']['404'].substitute(
     navbar = make_navbar( None )
    )
  )
  return page_404

@app.errorhandler(405)
def page_not_found_405(e):
  page_405 = TEMPLATES["_base"].substitute(
    title = "405 Error",
    description = str(e),
    body = TEMPLATES['errors']['405'].substitute(
     navbar = make_navbar( None )
    )
  )
  return page_405

@app.errorhandler(500)
def page_not_found_500(e):
  page_500 = TEMPLATES["_base"].substitute(
    title = "500 Error",
    description = str(e),
    body = TEMPLATES['errors']['500'].substitute(
     navbar = make_navbar( None )
    )
  )
  return page_500

@app.errorhandler(502)
def page_not_found_502(e):
  page_502 = TEMPLATES["_base"].substitute(
    title = "502 Error",
    description = str(e),
    body = TEMPLATES['errors']['502'].substitute(
     navbar = make_navbar( None )
    )
  )
  return page_502

 
if __name__ == "__main__":
    print(app.url_map) 
    app.run(host="0.0.0.0", port="5001", debug=True)
           