from macros import app
from flask import url_for, jsonify
import json


# Database / Middleware

@app.route('/')
def index():
    return jsonify({"foo": "bar"})