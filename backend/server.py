from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return {
        "status": "ok"
    }

@app.route("/login")
def login():
    return None 