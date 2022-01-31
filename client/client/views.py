from client import app
from flask import render_template, url_for, request
import requests, json
from collections import defaultdict

BASE_URI = 'http://127.0.0.1:5000/api/v1.0/foods'

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def index_form():

    queries = []
    nutrients = defaultdict(dict)
    data = request.form

    for item in data:
        if data[item]:
            outer, inner = item.split('_')
            nutrients[outer][inner] = data[item]

    queries = [ f'{nutrients[key]["type"]}={nutrients[key]["op"]}-{nutrients[key]["val"]}' for key in nutrients.keys() if nutrients[key].get('val', None) != None ]

    qstr = '&'.join(queries)
    URL = BASE_URI + '/query?' + qstr

    response = requests.get(URL)
    foods = response.json()

    return render_template('results.html', foods=foods, title="Foods")
