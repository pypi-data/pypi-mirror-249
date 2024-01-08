from kraken_schema_org import kraken_schema_org as k
from kraken_html.library import html


def form(url, record_type, language='EN-US', base_record=None, summary=True):
    """
    record_type: te type of the record for the form
    base_record: the initial values (default values) of the form
    summary: if True, returns only summary keys
    """

    base_record = base_record if isinstance(base_record, dict) else {}
    

    # Get fields for record_type

    if summary:
        keys = k.get_summary_keys(record_type)
    else:
        keys = k.get_keys(record_type)

    
    if not keys:
        return ''

    
    #Iterate through keys to generate form fields
    elements = []
    for key in keys:

        
        # Get html type
        html_type = k.key_get_html_types(key)
        html_type = html_type[0] if isinstance(html_type, list) and len(html_type) > 0 else 'text'
        label = key
        value = base_record.get(key, None)

        element = html.form_input(key, label, value, '', '', html_type)
        elements.append(element)

    # Generate form
    form_content = html.form(''.join(elements), url, 'Submit')

    return form_content