
import json
import copy

def to_list(record):
    """Convert dict to html
    """
    record = copy.deepcopy(record)

    if isinstance(record, list):
        count = 0
        content = '<dl class="row">'
        for i in record:
            html_v = to_list(i)
            content += f'''
            <dt class="col-sm-3">{str(count)}</dt>
            <dd class="col-sm-9">{html_v}</dd>
            '''
            count += 1
        content += '</dl>'
        return content
    
    elif isinstance(record, dict):
        content = '<dl class="row">'
        for k, v in record.items():
            html_v = to_list(v)
            content += f'''
            <dt class="col-sm-3">{k}</dt>
            '''
            v = v if isinstance(v, list) else [v]
            for v1 in v:
                html_v = to_list(v1)
                content += f'''
                <dd class="col-sm-9">{html_v}</dd>
                '''
        content += '</dl>'
        return content
    
    else:
        return record
        
def to_json(record):
    """Convert dict to html
    """

    record = copy.deepcopy(record)
    
    content = json.dumps(record, default=str, indent=4)
    content = content.replace('\n', '<br>')
    content = content.replace('    ', '&nbsp;&nbsp;&nbsp;&nbsp;')
    return content
