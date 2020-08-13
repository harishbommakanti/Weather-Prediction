from flask import Flask, render_template
from flask_cors import CORS, cross_origin

import time
import requests

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route("/")
def main():
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    return render_template("homepage.html")

if __name__ == "__main__":
    app.run()