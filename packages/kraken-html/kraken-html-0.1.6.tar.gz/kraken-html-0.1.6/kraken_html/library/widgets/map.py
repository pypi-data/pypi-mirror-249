from kraken_html.library import html


def map(record, mode='light', language='EN-US'):
    """
    """



    # 
    street = record.get('streetAddress', '')
    city = record.get('addressLocality', '')
    state = record.get('addressRegion', '')
    country = record.get('addressCountry', '')
    postalCode = record.get('postalCode', '')


    
   
    # Get map
    map_content = html.map(record) 
    
    

    # Generate list
    address_line1 = f'{city}, {state}, {postalCode}'
    address_content = ''
    address_content += _get_list_element(address_line1)
    address_content += _get_list_element(country)
    

    
    # Generate content
    content = f'''
    
<div class="card mb-3" style="height: 500px;" >
  <div class="row g-0 align-items-center">
    <div class="col-md-8">
    <div class="container-fluid google-maps text-center">
      {map_content}
      </div>
    </div>
    <div class="col-md-4">
      <div class="card-body">
        <h5 class="card-title">{str(street)}</h5>
        <ul class="list-unstyled">
            {address_content}
        </ul>
        </small></p>
      </div>
    </div>
  </div>
</div>
    '''
    return content



def _get_list_element(content):
    """
    """

    if not content or content == '':
        return ''

    content = str(content)
    
    content = f'''
    <li>{content}</li>
    '''
    return content

