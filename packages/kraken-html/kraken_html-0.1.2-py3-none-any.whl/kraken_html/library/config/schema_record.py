import json

def schema_record(record):
    """
    """
    json_content = json.dumps(record, default=str, indent=4)
    schema_content = f'<script type="application/ld+json">{json_content}</script>'

    return schema_content