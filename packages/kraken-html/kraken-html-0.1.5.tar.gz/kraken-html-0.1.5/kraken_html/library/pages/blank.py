from kraken_html.library import sections
from kraken_html.library import parts
from kraken_html.library import config

def blank(page_content, language='en'):
    """Blank page, mostly for testing purpose
    """

    if isinstance(page_content, list):
        page_content = ' '.join(page_content)

    
    content = f'''

        <!DOCTYPE html>
        <html  lang="{language}">
        
            <head>
                <meta charset="utf-8" >
                <title>Blank page</title>
                
                <!-- bootstrap css reqs -->
                {config.bootstrap_header()}
        
            </head> 
        
            <body>
        
                <!-- actual content of the web page -->
                {page_content}
        
                <!-- js scripts for bootstrap -->
                {config.bootstrap_body()}
        
            </body>
        
        </html>

    '''
    return content