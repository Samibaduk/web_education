import os

from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "Макс Волк кринж"


if __name__ == '__main__':
    port = 8080
    app.run(host='0.0.0.0', port=port)