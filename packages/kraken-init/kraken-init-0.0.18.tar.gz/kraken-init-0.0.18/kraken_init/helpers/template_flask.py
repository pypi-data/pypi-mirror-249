

def get_filename(name, directory=None):

    return f'{name}/flask_routes.py'


def get_content(name=None, directory=None):
    """
    """

    
    class_name = name.replace('kraken_', '')

    class_name = class_name.capitalize()
    class_name_collection = class_name + 's'
    
    dir = ''
    dir = directory.replace('/', '.') + '.' if directory else dir
    
    content = f'''


from flask import Flask
from flask import request
from flask import Response
from flask import redirect
from flask import url_for
from flask import jsonify
from {dir}{name}.helpers import json

from {dir}{name} import {name} as m
from {dir}{name}.Class_{name} import {class_name}
from {dir}{name}.Class_{name}s import {class_name_collection}

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
        r = {class_name}()
        records = r.autocomplete(key, '%' + str(value) + '%')
        return jsonify(records)


    content = "Api for {name}"
    return Response(content)


@app.route('/<key>/<value>', methods=['GET', 'POST'])
def search_path_get(key, value):

    r = {class_name}()
    records = r.search(key, '%' + value + '%')
    return jsonify(records)


@app.route('/autocomplete', methods=['GET', 'POST'])
def autocomplete_params_get():

    key = 'name'
    value = request.args.get(key)

    r = {class_name}()
    records = r.autocomplete(key, '%' + str(value) + '%')
    return jsonify(records)



@app.route('/autocomplete/<key>/<value>', methods=['GET', 'POST'])
def autocomplete_path_get(key, value):

    r = {class_name}()
    records = r.autocomplete(key, '%' + value + '%')
    return jsonify(records)


def run_api():
    app.run(host='0.0.0.0', debug=False)


    '''
    return content