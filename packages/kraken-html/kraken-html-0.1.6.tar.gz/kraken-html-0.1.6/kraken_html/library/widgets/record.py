
from kraken_html.library import html
from kraken_html.library import parts
from kraken_html.library import html_record



def record_item(record, mode='light'):
    """

    input record: https://schema.org/Rating
    """

    content = html.section(
        [
            html.title(
                html_record.record_names.get(record),
                'h1'
            ),
            html_record.to_list(
                html_record.html_record(record, True)
            )
        ]
    )
    
    return content
    
    
def test_record():
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
                    record_item(record)
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

    return record

def _get_code_content():
    code_content = '''
        from kraken_html.library import widgets
        record = {...}                          # Single or list of schema.org/rating
        content = widgets.testimonial(record)   # html content
        return Response(content)                
    '''
    return code_content