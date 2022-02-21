import b
from flask import Flask

app = Flask(__name__)
app.register_blueprint(b.simple_page)

if __name__ == "__main__":
    print(app.url_map)
    app.run(host="0.0.0.0", port="5001", debug=True)