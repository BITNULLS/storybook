"""
app.py
    Main launch point for our web server.
"""

from flask import Flask
from api import main
import admin
import index
import login
import password
import register
import story_selection
import storyboard


app = Flask(__name__, static_url_path="/static/", static_folder="static")

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
    app.run(host="0.0.0.0", port="5001", debug=True)