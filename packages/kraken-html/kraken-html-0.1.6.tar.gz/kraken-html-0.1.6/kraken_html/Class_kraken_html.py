
    
import copy
from kraken_html.helpers import json
import os
import pkg_resources
from kraken_html import kraken_html as m

"""
Notes:
To access files in data directory, use:
new_path = pkg_resources.resource_filename('kraken_html', old_path)

"""
    
class Html:
    """
    The Vehicle object contains a lot of vehicles

    Args:
        arg1 (str): The arg is used for...
        arg2 (str): The arg is used for...
        arg3 (str): The arg is used for...

    Attributes:
        record (dict): This is where we store attributes
        json (str): Record in json format
        
    """

    def __init__(self, config=None):
        self._record = {}

        if config:
            self._record = config
        else:
            self._record = self.get_base_config()
        

    def __str__(self):
        """
        """
        return str(self._record)

    
    def __repr__(self):
        """
        """
        return str(self._record)

    
    def __eq__(self, other):
        """
        """
        if type(self) != type(other):
            return False
            
        if self._record == other._record:
            return True
        return False

    def __gt__(self, other):
        """
        """
        return True


    def add_header(self, headline, url):
        """Add an element to the header
        """

        element =  {
            '@type': 'SiteNavigationElement',
            'headline': headline,
            'url': url
        }

        parts = self._record.get('hasPart', [])
        for i in parts:
            if i.get('@type', None) == 'WPHeader':
                i['hasPart'].append(element)
                return

    def add_footer(self, headline, url):
        """Add an element to the header
        """

        element =  {
            '@type': 'SiteNavigationElement',
            'headline': headline,
            'url': url
        }
        
        parts = self._record.get('hasPart', [])
        for i in parts:
            if i.get('@type', None) == 'WPFooter':
                i['hasPart'].append(element)
                return

    @property
    def brand(self):
        return self._record.get('subjectOf', {}).get('brand', {}).get('name', None)
    @brand.setter
    def brand(self, value):
        self._record['subjectOf']['brand']['name'] = value
    
    @property
    def legalName(self):
        return self._record.get('subjectOf', {}).get('legalName', None)
    @legalName.setter
    def legalName(self, value):
        self._record['subjectOf']['legalName'] = value


    def webpage(self, content):
        """
        """
        return m.pages.base(self._record, content)
        
    
    def set(self, property, value):
        """
        """
        self._record[property] = value
        return True

    
    def get(self, property):
        """
        """
        return self._record.get(property, None)

    
    def load(self, value):
        """
        """
        self._record = value
        return True


    def dump(self): 
        """
        """
        return copy.deepcopy(self._record)
        

    def set_json(self, value):
        """
        """
        record = json.loads(value)
        self.load(record)
        return True

    def get_json(self):
        """
        """
        return json.dumps(self.dump())

    @property
    def record(self):
        return self.dump()

    @record.setter
    def record(self, value):
        return self.load(value)
    
    @property
    def json(self):
        return self.get_json()

    @json.setter
    def json(self, value):
        return self.set_json(value)
        

    def search(self, value=None, value2=None):
        return 1


    def get_base_config(self):
        """
        """
        config = {
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
                            'headline': 'Privacy Policy',
                            'url': '/privacy_policy'
                        },
                        {
                            '@type': 'SiteNavigationElement',
                            'headline': 'Terms and conditions',
                            'url': '/terms_and_conditions'
                        },
                        {
                            '@type': 'SiteNavigationElement',
                            'headline': 'Contact us',
                            'url': '/contact_us'
                        }
                    ]
                }
            ]

        }
        return config
        