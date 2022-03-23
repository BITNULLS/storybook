"""
app.py
    Main launch point for our web server.
"""
import os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import sys
sys.path.append(ROOT_DIR) # Adds higher directory to python modules path.

from flask import Flask

from edu_storybook.core.config import config
from edu_storybook.api import main
from edu_storybook import admin
from edu_storybook import index
from edu_storybook import login
from edu_storybook import password
from edu_storybook import register
from edu_storybook import story_selection
from edu_storybook import storyboard

import logging

app = Flask('edu_storybook', static_url_path="/static/", static_folder="static")

test_client = app.test_client()

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
app.logger.addHandler(handler)
app.logger.setLevel(logging.DEBUG)
app.logger.debug('Starting app')

app.register_blueprint(main.api) 
app.register_blueprint(admin.admin)
app.register_blueprint(index.homepage)
app.register_blueprint(login.login)
app.register_blueprint(password.password)
app.register_blueprint(register.register)
app.register_blueprint(story_selection.story_selection)
app.register_blueprint(storyboard.storyboard)

if __name__ == "__main__":
    print(app.url_map) 
    del test_client
    app.run(host="0.0.0.0", port="5001", debug=True)
           