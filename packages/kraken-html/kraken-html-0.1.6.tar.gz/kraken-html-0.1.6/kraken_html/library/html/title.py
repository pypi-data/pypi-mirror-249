

def title(text, level = 'H1'):
    content = '''
        <{level} class="pb-xl-1 pt-xl-5">{text}</{level}>
        '''.format(
            text = text,
            level = level
        )
    
    return content