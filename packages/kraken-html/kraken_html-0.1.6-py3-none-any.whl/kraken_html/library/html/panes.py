
def panes(items):

    element_content = ''
    for i in items:
        element_content += f'<div class="col-lg-4">{i}</div>'
    
    content = f'''
    
    <div class="row">{element_content}</div>
    
    
    '''

    return content