


def pricing(offers, theme='dark'):
    """
    """


    offer = {
        '@type': 'offer',
        'headline': 'offer1',
        'text': '',
        'features': ['awesome', 'spectacular', 'extraordinary'],
        'price': '480',
        'cta': 'Get it now'

    }
    offers = [offer, offer, offer, offer]


    content = f'''
    
    <div class="container py-3 bg-{theme} text-bg-{theme}" data-bs-theme="{theme}" data-aos="fade-down" data-aos-delay="200">
    <div class="row row-cols-1 row-cols-md-{str(len(offers))} mb-3 text-center">
      {_get_pricing(offers)}
    </div>
    </div>
    
    '''
   
    return content


def _get_pricing(offers):
    """
    """
    content = ''
    for offer in offers:
        offer_content = f'''
        <div class="col">
            <div class="card mb-4 rounded-3 shadow-sm">
              <div class="card-header py-3">
                <h4 class="my-0 fw-normal">{offer.get('headline', None)}</h4>
              </div>
              <div class="card-body">
                <h1 class="card-title pricing-card-title">${offer.get('price', None)}<small class="text-body-secondary fw-light">/mo</small></h1>
                <ul class="list-unstyled mt-3 mb-4">
                  {_get_features(offer.get('features', None))}
                </ul>
                <button type="button" class="w-100 btn btn-lg btn-primary">{offer.get('cta', None)}</button>
              </div>
            </div>
          </div>
        
        '''
        content += offer_content
    
    return content


def _get_features(features):
    '''
    
    '''
    content = ''
    for i in features:
        content += f'<li>{i}</li>'

    return content