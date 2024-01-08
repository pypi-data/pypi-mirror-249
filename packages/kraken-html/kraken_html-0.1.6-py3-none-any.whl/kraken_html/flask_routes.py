


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

from kraken_schema_org import kraken_schema_org as k


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
        website_config = {
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
                            'headline': 'Main',
                            'url': '/main'
                        },
                        {
                            '@type': 'SiteNavigationElement',
                            'headline': 'Confidentiality',
                            'url': '/confidentiality'
                        }
                    ]
                }
            ]

        }

        site = Html()
        site.brand = 'Test brand'
        site.legalName = 'Test brand Inc.'
        site.add_footer('test1', '/test1')
        site.add_footer('test2', '/test2')

        
        
        action = {
            '@type': 'action',
            'name': 'Test action',
            'url': '/'
        }

        content = m.sections.search(action)
        
        page_content = m.pages.base(website_config,content)

        page_content = site.webpage(content)
        
        return Response(page_content)

    
    if 1==0:

        content = ''
        
        record = {
            '@type': "person",
            "@id": "abc123",
            "givenName": "Bob",
            "familyName": "Smith",
            "url": "https://www.test.com",
            'telephone': "15146073437",
            "email": "bob@test.com",
            'title': 'kick_ass in chief', 
            "worksFor": {
                '@type': "organization",
                '@id': "test_org",
                "name": "Test Org",
                "url": "https://www.test_org.com/"
            }
        }


        address= k.get_data('postalAddress')
        content += m.widgets.map(address)

        record = k.get_data('Person')
        record = k.normalize_record(record)
        record['name'] = k.get_record_name(record)

        content += m.widgets.person(record)

        url = 'https://www.test.com'
        content += m.form.form(url, 'person', 'EN-US', record)
        
        page_content = m.pages.blank(content)
        
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


    