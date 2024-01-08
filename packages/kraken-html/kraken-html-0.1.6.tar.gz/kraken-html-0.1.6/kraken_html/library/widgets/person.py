from kraken_html.library import html


def person(record, mode='light', language='EN-US'):
    """
    """



    # 
    image_url = record.get('image', None)
    givenName = record.get('givenName', None)
    familyName = record.get('familyName', None)
    title = record.get('title', None)
    email = record.get('email', None)
    phone = record.get('telephone', None)

    worksFor = record.get('worksFor', {})
    worksFor_name = worksFor.get('name', None)
    worksFor_url = worksFor.get('url', None)
    
    # Get profile picture
    profile_picture = html.image(image_url, None) if image_url else html.anon()
    
    # Apply styling
    worksFor_url = html.link(worksFor_url, worksFor_url, True)
    title = f'<strong>{title}</strong>'

    # Generate list
    contact_content = ''
    contact_content += _get_list_element(title)
    contact_content += _get_list_element(worksFor_name)
    contact_content += _get_list_element(phone)
    contact_content += _get_list_element(email)
    contact_content += _get_list_element(worksFor_url)

    
    # Generate content
    content = f'''
<div class="card mb-3" style="max-width: 400px;">
  <div class="row g-0 align-items-center">
    <div class="col-md-4">
    <div class="container text-center">
      {profile_picture}
      </div>
    </div>
    <div class="col-md-8">
      <div class="card-body">
        <h5 class="card-title">{str(givenName)} {str(familyName)}</h5>
        <ul class="list-unstyled">
            {contact_content}
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

