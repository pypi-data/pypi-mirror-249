import json

from kraken_html.library import html
from kraken_html.library import parts
from kraken_html.library import html_record



def testimonial(record, mode='light'):
    """

    input record: https://schema.org/Rating
    """


    # Handle lists:
    if isinstance(record, list):
        cards = []
        for i in record:
            cards.append(testimonial(i))
        return html.cardgrid(cards)

    # Initialize body content
    body_content = ''
    
    # Get star rating
    body_content += _get_rating(record, mode)

    # Get author
    body_content += _get_citation(record, mode)

    # Get citation content
    body_content += _get_name_title(record, mode)


    # Put into card
    content = html.card(None, body_content, None)
    

    return content


def _get_rating(record, mode='light'):
    """
    """
    rating_value = record.get('ratingValue', None) 

    if not rating_value:
        return ''

    content = f'<p>{html.rating(rating_value)}</p>'

    return content


def _get_citation(record, mode='light'):
    """
    """

    ratingExplanation = record.get('ratingExplanation', None) 

    content = f'<p>"{ratingExplanation}"</p>'

    return content
        


def _get_name_title(record, mode='light'):
    """
    """
    author = record.get('author', {}) 
    given_name = author.get('givenName', None)
    family_name = author.get('familyName', None)
    author_name = f'{given_name} {family_name}'
    jobTitle = author.get('jobTitle', None)
    

    content = ''
    if author_name is not None and author_name != '':
        content += f'<h4>{author_name}</h4>'

    if jobTitle is not None and jobTitle != '':
        content += f'<p class="fs-6 mb-0">{jobTitle}</p>'

    return content





def test_testimonial():
    """
    """

    content = html.section(
        [
            _test_code_content(),
            _test_testimonial_single(),
            _test_testimonial_multiple()
        ]
    )
    
    

    return content

def _test_code_content():
    """
    """
    code_content = '''
    from kraken_html.library import widgets
    record = {...}                          # Single or list of schema.org/rating
    content = widgets.testimonial(record)   # html content
    return Response(content)                
    '''
    content = html.section(
        [
            html.title('Code', 'h2'),
            html.code(code_content)
        ]
    )
    return content

def _test_testimonial_single():
    
    
    record = _get_record()

    content = html.section(
        [
            html.div(
                html.title('Single record', 'h2')
            ),
            html.div(
                html.accordion('Record', html_record.to_json(record))
            ),
            html.div(
                html.title('widget', 'h3')
            ),
            html.div(
                testimonial(record)
            )
        ]
    )
   
    return content


def _test_testimonial_multiple():

    record = _get_record()
    record = [record, record, record]

    content = html.section(
        [
            html.div(
                html.title('Multiple records', 'h2')
            ),
            html.div(
                html.accordion('Records', html_record.to_json(record))
            ),
            html.div(
                html.title('widget', 'h3')
            ),
            html.div(
                testimonial(record)
            )
        ]
    )

    return content



def _get_record():
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