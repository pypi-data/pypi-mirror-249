

def form(content, action, action_text='Submit'):
    
    
    content = f'''
        <form action="{action}" method="post">
         {content}
         <input type="submit" value="{action_text}">
        </form>
    '''

    return content


