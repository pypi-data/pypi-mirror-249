
from kraken_html.library import html

def header(record):
    """
    """


    subjectOf = record.get('subjectOf', {})
    legal_name = subjectOf.get('legalName', None)
    brand = subjectOf.get('brand', {})
    brand_name = brand.get('name', '')

    parts = record.get('hasPart', [])
    links = []
    for i in parts:
        if i.get('@type', None) == 'WPHeader':
            links = i.get('hasPart', [])


    content = html.html_nav(brand_name, links)
    return content