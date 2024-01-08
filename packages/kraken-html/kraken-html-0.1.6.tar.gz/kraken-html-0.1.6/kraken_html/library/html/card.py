

def card(header=None, body=None, footer=None):
    """content - html fo the content
    title - text
    url - url for link
    """

    content = f'''
<div class="card h-100">
    {header_content(header)}
    {body_content(body)}
    {footer_content(footer)}
</div>    
'''
    return content



def header_content(initial_content):
    """
    """
    if initial_content is None or initial_content == '':
        return ''
    
    content = f'''
<div class="card-header">
    {initial_content}
</div>
    '''
    return content


def body_content(initial_content):
    """
    """
    if initial_content is None or initial_content == '':
        return ''

    content = f'''
<div class="card-body">
    {initial_content}
</div>
    '''
    return content


def footer_content(initial_content):
    """
    """
    if initial_content is None or initial_content == '':
        return ''

    content = f'''
<div class="card-footer">
    {initial_content}
</div>
    '''
    return content
