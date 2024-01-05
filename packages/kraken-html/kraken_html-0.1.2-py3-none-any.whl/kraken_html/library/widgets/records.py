
from kraken_html.library import html
from kraken_html.library import parts
from kraken_html.library import html_record

import copy

def record_items(records, mode='light'):
    """

    input record: https://schema.org/Rating
    """

    new_records = []
    for i in records:
        new_record = copy.deepcopy(i)
        new_record['name'] = html_record.record_names.get(i)
        new_records.append(new_record)

    keys = ['@type', '@id', 'name', 'url']
    
    content = html.section(
        [
            html.title(
                'Records', 'h1'
            ),
            html.table(
                html_record.html_record(new_records, False),
                keys
            )
        ]
    )
    
    return content
    
    
def test_records():
    """
    """
    
    record = _get_test_record()

    content = html.section(
        [
            html.title(
                'Record widget', 'h1'
            ),
            
            html.div(
                [
                    html.title(
                        'Code', 'h2'
                    ),
                    html.code(
                        _get_code_content()
                    )
                ]
            ),
            html.div(
                [
                    html.title(
                        'Record Record', 'h2'
                    ),
                    html.accordion('Record example', html_record.to_json(record))
                ]
            ),
            html.div(
                [
                    html.title(
                        'Record widget', 'h2'
                    ),
                    record_items(record)
                ]
            )
        ]
    )

    return content
        



def _get_test_record():
    record = {
        '@type': 'Rating',
        '@id': 'test_testimonial',
        'author': {
            '@type': 'person',
            '@id': 'reviewer1',
            'givenName': 'John',
            'familyName': 'Smith',
            'jobTitle': 'Director engineering'
        },
        'ratingValue': 3.5,
        'ratingExplanation': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. '
    }

    records = [record,record,record,record,record,record,record,record]
    
    return records

def _get_code_content():
    code_content = '''
        from kraken_html.library import widgets
        record = {...}                          # Single or list of schema.org/rating
        content = widgets.testimonial(record)   # html content
        return Response(content)                
    '''
    return code_content