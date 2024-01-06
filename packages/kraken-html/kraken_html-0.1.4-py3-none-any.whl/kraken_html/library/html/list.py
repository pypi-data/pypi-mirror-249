


def get_list(record, level=0):

    sub_content = ''
    print('----')
    print(record)
    print('----')
    for k, v in record.items():
        sub_content += get_list_row(k, v)


    content = f'''
        
        <div class="container-fluid">
        <dl class="row mb-0">
            {sub_content}
        </dl>
        </div>
        
    
    '''
    return content


def get_list_row(key, value, leve=0):
    """
    """
    content = f'''

        <dl class="row mb-0">
          <dt class="col-sm-2 mb-0">{key}</dt>
          <dd class="col-sm-10 mb-0">
          {get_list_items(value)}
          </dd>
        </dl>
    
    
    '''
    return content

def get_list_items(value, level=0):
    """
    """
    value = value if isinstance(value, list) else [value]
    content = '<ul class="list-unstyled mb-0">'

    for v in value:
        if 1==0:
            if isinstance(v, dict) and level < 2:
    
                content += f'''
                <details>
                    <summary>{str(v.get('@type', None)) + '/' + str(v.get('@id', None))}</summary>
    
                    <p>{get_list(v, level + 1)}</p>
                </details>
                
                
                '''
                
                #content += get_list(v, level + 1)
    
            else:
                if len(value) == 1:
                    content += v
                else:
                    content += f'''
                        <li mb-0>{v}</li>
                '''
        if not v:
            continue
            
        if len(value) == 1:
            content += v
        else:
            content += f'''
                <li mb-0>{v}</li>
                '''
            
    content += '</ul>'
    return content


