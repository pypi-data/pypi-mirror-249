
def link(url, text, new_tab = None):
    """Converts a url and text into a html link
    """

    if not url:
        return ''
    
    if new_tab:
        link = f'<a href="{url}" target="_blank">{text}</a>'
    else:
        
        link = f'<a href="{url}">{text}</a>'
    return link
