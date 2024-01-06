


from flask import Flask
from flask import request
from flask import Response
from flask import redirect
from flask import url_for
from flask import jsonify
from kraken_boilerplate.helpers import json

from kraken_boilerplate import kraken_boilerplate as m
from kraken_boilerplate.class_kraken_boilerplate import Boilerplate
from kraken_boilerplate.class_kraken_boilerplates import Boilerplates

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


    record = {
        '@type': 'WebSite',
        'name': 'UNSPSC Codes',
        'subjectOf': {
            '@type': 'organization',
            'name': 'Data Factory',
            'legalName': 'Data Factory Inc.',
            'brand': {
                '@type': 'brand',
                'name': 'Data Factory',
                'logo': 'http://logo_url.com'
            }
        },
        'privacy': {
            'email': 'privacy@test.com',
        },
        'url': 'https://unspsc_codes.com',
        'hasPart':[

            {
                '@type': 'WPHeader',
                'hasPart': [
                    {
                        '@type': 'SiteNavigationElement',
                        'headline': 'Home',
                        'url': '/main'
                    }

                ]
            },
            {
                '@type': 'WPFooter',
                'hasPart': [
                    {
                        '@type': 'SiteNavigationElement',
                        'headline': '',
                        'url': '/main'
                    }
                ]
            }
        ]

    }

    
    content = m.get('terms', record)
    return Response(content)


@app.route('/<key>/<value>', methods=['GET', 'POST'])
def search_path_get(key, value):

    r = Boilerplate()
    records = r.search(key, '%' + value + '%')
    return jsonify(records)


@app.route('/autocomplete', methods=['GET', 'POST'])
def autocomplete_params_get():

    key = 'name'
    value = request.args.get(key)

    r = Boilerplate()
    records = r.autocomplete(key, '%' + str(value) + '%')
    return jsonify(records)



@app.route('/autocomplete/<key>/<value>', methods=['GET', 'POST'])
def autocomplete_path_get(key, value):

    r = Boilerplate()
    records = r.autocomplete(key, '%' + value + '%')
    return jsonify(records)


def run_api():
    app.run(host='0.0.0.0', debug=False)


    