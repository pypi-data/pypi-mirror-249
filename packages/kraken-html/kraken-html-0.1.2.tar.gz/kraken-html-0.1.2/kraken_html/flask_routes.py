


from flask import Flask
from flask import request
from flask import Response
from flask import redirect
from flask import url_for
from flask import jsonify
from kraken_html.helpers import json

from kraken_html import kraken_html as m
from kraken_html.Class_kraken_html import Html
from kraken_html.Class_kraken_htmls import Htmls




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


    if 1==1:
        page_content = m.pages.blank(
            m.get_catalog()
        )
        
        return Response(page_content)

    
    key = 'name'
    value = request.args.get(key)

    if value:
        r = Html()
        records = r.autocomplete(key, '%' + str(value) + '%')
        return jsonify(records)

    header = {'headline': 'Test headline', 'text': 'some text'}

    content = m.sections.pricing('r')
    content += m.sections.hero(header)
    page_content = m.pages.base(content)
    
    
    #content = "Api for kraken_html"
    return Response(page_content)


@app.route('/<key>/<value>', methods=['GET', 'POST'])
def search_path_get(key, value):

    r = Html()
    records = r.search(key, '%' + value + '%')
    return jsonify(records)


@app.route('/autocomplete', methods=['GET', 'POST'])
def autocomplete_params_get():

    key = 'name'
    value = request.args.get(key)

    r = Html()
    records = r.autocomplete(key, '%' + str(value) + '%')
    return jsonify(records)



@app.route('/autocomplete/<key>/<value>', methods=['GET', 'POST'])
def autocomplete_path_get(key, value):

    r = Html()
    records = r.autocomplete(key, '%' + value + '%')
    return jsonify(records)

@app.route('/test', methods=['GET', 'POST'])
def test_get(key, value):


    content = m.get_catalog()
    page_content = m.pages.blank(content)
    
    return Response(page_content)


def run_api():
    app.run(host='0.0.0.0', debug=False)


    