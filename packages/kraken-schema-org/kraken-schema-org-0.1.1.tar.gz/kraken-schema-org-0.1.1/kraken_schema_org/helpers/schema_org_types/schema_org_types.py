from functools import lru_cache
from kraken_schema_org.helpers import schema_org_website_data as w 

def get_python_types(key):
    """
    """

    types = []

    datatypes = get_jsonld_types(key)
    if not datatypes:
        return []
    
    for i in datatypes:

        t = i.lower().replace('schema:', '')

        if t == 'object':
            types.append('object')
            
        if t == 'text':
            types.append('str')

        if t == 'number':
            types.append('float')

        if t == 'date':
            types.append('str')

        if t == 'time':
            types.append('str')

        if t == 'boolean':
            types.append('bool')

        if t == 'datetime':
            return 'datetime.datetime'
        else:
            return 'dict'

    return types



def get_json_types(key):
    """Returns the json schema types available for a key
    """
    types = []

    datatypes = get_jsonld_types(key)
    if not datatypes:
        return []
    
    for i in datatypes:

        t = i.lower().replace('schema:', '')

        if t == 'object':
            types.append('object')
            
        if t == 'text':
            types.append('string')
    
        if t == 'number':
            types.append('number')
            
        if t == 'date':
            types.append('string')
          
        if t == 'time':
            types.append('string')

        if t == 'boolean':
            types.append('boolean')
           
        if t == 'datetime':
            return 'string'
        else:
            return 'object'
    
    return types


def get_html_types(key):
    """
    """

    types = []
    for i in get_jsonld_types(key):
        if i in ['object']:
            types.append('object')
        if i in ['URL']:
            types.append('url')
        if i == ['DateTime']:
            types.append('datetime-local')
        if i in ['Date']:
            types.append('date')
        if i in ['Time']:
            types.append('time')
        if i in ['Number']:
            types.append('number')
        if i in ['Boolean']:
            types.append('checkbox')
        if i in ['Text']:
            if key in ['telephone']:
                types.append('tel')
            if key in ['email']:
                types.append('email')
    return types


@lru_cache(maxsize=32)
def get_jsonld_types(key):
    """Return the jsonld(schema.org) types that this attribute can possess
    """
    
    record = w.get_property_definition(key)

    print('propdef', key, record)
    
    if not record:
        # Test if class, if so return object
        print('w', key, w.get_class(key))
        if w.get_class(key):
            
            return ['object']
        else:
            return None

    
    ranges = record.get("schema:rangeIncludes", [])
    ranges = ranges if isinstance(ranges, list) else [ranges]
    print('ranges', ranges)

    ranges = [x.get('@id', '').replace('schema:', '') for x in ranges]

    return ranges


