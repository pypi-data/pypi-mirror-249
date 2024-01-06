
from kraken_html.library import sections
from kraken_html.library import parts
from kraken_html.library import config

def base(website_record, page_content, schema_record={}, language='en'):
    """
    """
    
    name = website_record.get('name', None)
    favicon_url = website_record.get('thumbnailUrl', None)
    

    
    website_record = {
        '@type': 'WebSite',
        'hasPart':[

            {
                '@type': 'WPHeader',
                'hasPart': [
                    {
                        '@type': 'SiteNavigationElement',
                        'headline': 'Home',
                        'url': '/main'
                    }
                    
                ]
            },
            {
                '@type': 'WPFooter',
                'hasPart': [
                    {
                        '@type': 'SiteNavigationElement',
                        'headline': '',
                        'url': '/main'
                    }
                ]
            }
        ]
        
    }

    content = f'''
    
<!DOCTYPE html>
<html  lang="{language}">
    
    <head>
        <meta charset="utf-8" >
        <title>{name}</title>
        <link rel="icon" href="{favicon_url}">
        
        <!-- bootstrap css reqs -->
        {config.bootstrap_header()}

        <!-- schema.org info -->
        {config.schema_record(schema_record)}
        
    </head> 
    
    <body>

        <!-- nav_bar -->
        {sections.nav_bar(website_record)}

        <!-- actual content of the web page -->
        {page_content}

        <!-- js scripts for bootstrap -->
        {config.bootstrap_body()}

    </body>

</html>

    
    '''
    return content