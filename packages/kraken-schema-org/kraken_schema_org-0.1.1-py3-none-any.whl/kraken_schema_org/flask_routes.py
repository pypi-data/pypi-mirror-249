


from flask import Flask
from flask import request
from flask import Response
from flask import redirect
from flask import url_for
from flask import jsonify
from kraken_schema_org.helpers import json

from kraken_schema_org import kraken_schema_org as m
from kraken_schema_org.Class_kraken_schema_org import Schema_org
from kraken_schema_org.Class_kraken_schema_orgs import Schema_orgs

UPLOAD_FOLDER = '/path/to/the/uploads'

# Initialize flask app
app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')
app.secret_key = b'_5#mn"F4Q8znxec]/'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def main_get():

    key = 'name'
    value = request.args.get(key)

    if value:
        r = Schema_org()
        records = r.autocomplete(key, '%' + str(value) + '%')
        return jsonify(records)


    content = "Api for kraken_schema_org"
    return Response(content)


@app.route('/<key>/<value>', methods=['GET', 'POST'])
def search_path_get(key, value):

    r = Schema_org()
    records = r.search(key, '%' + value + '%')
    return jsonify(records)


@app.route('/autocomplete', methods=['GET', 'POST'])
def autocomplete_params_get():

    key = 'name'
    value = request.args.get(key)

    r = Schema_org()
    records = r.autocomplete(key, '%' + str(value) + '%')
    return jsonify(records)



@app.route('/autocomplete/<key>/<value>', methods=['GET', 'POST'])
def autocomplete_path_get(key, value):

    r = Schema_org()
    records = r.autocomplete(key, '%' + value + '%')
    return jsonify(records)


def run_api():
    app.run(host='0.0.0.0', debug=False)


    