

from kraken_schema_org.helpers.schema_org_website_data import schema_org_website_data as w


def get_json_schema(record_type, level=0):
    """
    """

    # Retrieve json-ld schema
    schema = w.get_schema(record_type)

    # Initiate new object
    object = {
        "title": record_type,
        "description": "",
        "type": "object",
        "properties": {
            "@type": {
                "type": "string"
            },
            "@id": {
                "type": "string"
            }
        }
    }
    
    
    # Iterate through keys
    for k, v in schema.items():

        domains = v.get('schema:domainIncludes', [])
        domains = domains if isinstance(domains, list) else [domains]


        object['properties'][k] = {
            'type': 'array',
            'items': {
                "oneOf": []
            }
        }

        
        for d in domains:
            
            property_name = d.get('@id', None)
            t = _get_type(property_name)

            if t == 'object':
                if level < 1:
                    p = get_json_schema(property_name, level + 1)
                else:
                    p = {
                        "type": "object",
                        "properties": {
                            "@type": {
                                "type": "string"
                                },
                            "@id": {
                                "type": "string"
                                }
                            }
                        }
            else:
                p = {
                    "type": t
                }

            object['properties'][k]['items']['oneOf'].append(p)
                          
    return object


def _get_type(record_type):
    
    t = record_type.lower().replace('schema:', '')
    
    if record_type == 'text':
        return 'string'
    
    if record_type == 'number':
        return 'number'
    if record_type == 'date':
        return 'string'
    if record_type == 'time':
        return 'string'
    if record_type == 'boolean':
        return 'boolean'
    if record_type == 'datetime':
        return 'string'
    else:
        return 'object'
                



