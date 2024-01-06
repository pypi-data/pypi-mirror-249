

def paragraph(content):
    """
    """

    if isinstance(content, list):
        content = ' '.join(content)

    
    content = f'<p>{content}</p>'
    return content