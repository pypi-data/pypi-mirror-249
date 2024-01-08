
from kraken_html.library import html

def footer(record):
    """
    """

    subjectOf = record.get('subjectOf', {})
    legal_name = subjectOf.get('legalName', None)
    brand = subjectOf.get('brand', {})
    brand_name = brand.get('name', '')

    parts = record.get('hasPart', [])
    links = []
    for i in parts:
        if i.get('@type', None) == 'WPFooter':
            links = i.get('hasPart', [])
    

    content = html.footer(legal_name, brand_name, links)
    return content

    
