


def section(content=None):
    """
    """
    
    if isinstance(content, list):
        content = ' '.join(content)

    
    section_content = f'''
<section>
    {content}
</section>
    '''

    return section_content