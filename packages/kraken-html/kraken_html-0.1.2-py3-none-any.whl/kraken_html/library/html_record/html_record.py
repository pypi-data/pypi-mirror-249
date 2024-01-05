
from kraken_html.library import html
from kraken_html.library.html_record import record_names as thing_names
import uuid

def html_record(value, expand=False):
    # Returns dict with enhanced values


    if not value:
        return None

    if isinstance(value, list):
        new_v = [html_record(x, expand) for x in value]
        return new_v


    # Buidld new dict
    new_record = {}
    for key, values in value.items():

        new_record[key] = []
        values = [values] if not isinstance(values, list) else values



        for v in values:

            new_value = v

            if isinstance(v, dict):
                if '@type' in v.keys() and key:
                    if not expand:
                        new_value = html_value_record_ref(v)
                    else:
                        new_value = html_record_expandable_section(v)

            elif key and 'thumbnailUrl' in key:
                new_value = html_value_thumbnail(v)

            elif key and 'url' in key:
                new_value = html_value_url(v)

            elif key == '@type':
                new_value = html_value_type(v)

            elif key == '@id':
                new_value = html_value_id(value)

            else:
                new_v = v
                new_value = new_v

            new_record[key].append(new_value)

    return new_record



def html_record_expandable_section(value):
    """
    """
    summary = html_value_record_ref(value)
    new_record = html_record(value, True)

    details = html.get_list(new_record)

    content = html.summary(summary, details)
    return content



def html_value_record_ref(value):

    name = thing_names.get(value)

    t = value.get('@type', None)
    i = value.get('@id', None)



    t = t if not isinstance(t, list) else t[0]
    i = i if not isinstance(i, list) else i[0]

    link = '/' + str(t) + '/' + str(i)

    if not name:
        name = link

    for k, v in value.items():
        if 'name' in k.lower():
            if not isinstance(v, list):
                v = [v]
            if len(v) > 0:
                name = v[0]

    new_v = html.link(link, name)
    return new_v


def html_value_type(record_type):
    # Add link to types
    if isinstance(record_type, list) and len(record_type) > 0:
        record_type = record_type[0]
    new_v = html.link('/' + str(record_type), record_type)
    return new_v

def html_value_id(record):
    # Add link to types
    record_type = record.get('@type', None)
    if isinstance(record_type, list) and len(record_type) > 0:
        record_type = record_type[0]
    record_id = record.get('@id', None)
    if isinstance(record_id, list) and len(record_id) > 0:
        record_id = record_id[0]

    # Escape record id


    new_v = html.link('/' + str(record_type) + '/' + str(record_id), str(record_id))
    return new_v

def html_value_url(value):
    # Add link to url
    new_v = html.link(value, value)
    return new_v

def html_value_thumbnail(url):
    # Returns image with a link

    modal_id = 'ref_' + str(uuid.uuid4())
    image = html.image(url, None, 'xxs', None, modal_id)

    modal_content = html.image(url, None, 'xxl')
    modal = html.get_modal(modal_id, modal_content)

    content = image + modal



    return content