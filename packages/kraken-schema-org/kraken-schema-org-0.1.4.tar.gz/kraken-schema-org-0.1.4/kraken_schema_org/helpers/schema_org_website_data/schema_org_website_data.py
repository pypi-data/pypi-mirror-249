import json
from functools import lru_cache 
import requests 
from kraken_schema_org.helpers.kraken_db import Kraken_db


db_definitions = Kraken_db('data/definitions.json')

db_class = Kraken_db('data/classes.json')
db_properties = Kraken_db('data/properties.json')
db_schemas = Kraken_db('data/schemas.json')
db_properties_definition = Kraken_db('data/properties_definition.json')


base_schemas = ['website', 'webpage', 'person', 'organization', 'imageobject', 'thing', 'action', 'product']



def get_key(key=None):
    """Given a key name, returns the correctly spelled property (same as get_property)
    """
    return get_property(key)

@lru_cache(maxsize=32)
def get_property(property_name=None):
    """Given a property name, returns the correctly spelled property
    """
    if len(db_properties) == 0:
        _init()

    if not property_name:
        return list(db_properties.get().values())

    
    property_name = property_name.replace('schema:', '')
    property_name = property_name.lower()
    
    return db_properties.get(property_name)


@lru_cache(maxsize=32)
def get_property_definition(property_name=None):
    """Given a property name, returns the correctly spelled property
    """
    if len(db_properties) == 0:
        _init()

    if not property_name:
        return list(db_properties.get().values())

    property_name = get_property(property_name)
    
    return db_properties_definition.get(property_name)



def get_record_type(record_type):
    """Given a class name, returns the correctly spelled class (same as get_class)
    """
    return get_class(record_type)


def get_class(class_name=None):
    """Given a class name, returns the correctly spelled class
    """
    if len(db_class) == 0:
        _init()

    # If provided with a dict, retrieves class_name from dict
    class_name = class_name if not isinstance(class_name, dict) else class_name.get('@type', None)
    
    return _get_class(class_name)

@lru_cache(maxsize=32)
def _get_class(class_name):
    # Returns all if blank
    if not class_name:
        return list(db_class.get().values())

    # normalize class_name
    class_name = class_name.replace('schema:', '')
    class_name = class_name.lower()

    # Return 
    return db_class.get(class_name)
    
@lru_cache(maxsize=32)
def get_schema(record_type):
    """
    """

    class_name = get_class(record_type)
    record = db_schemas.get(class_name)

    if not record:
        _download_schema_from_schema_org(class_name)
        record = db_schemas.get(class_name)
    
    record = record if record else {} 
    return record

@lru_cache(maxsize=32)
def get_keys(record_type):
    """
    """

    record = get_schema(record_type)

    if not record:
        return None
    return list(record.keys())
        

def _init():
    """Load preliminary data
    """

    print('Initializing base data')
    
    _download_base_data_from_schema_org()

    for i in base_schemas:
        get_schema(i)
    
        
    return

def _download_base_data_from_schema_org():
    """Download schema_org vocabulary definition file data
    """

    url = 'https://schema.org/version/latest/schemaorg-current-https.jsonld'
    r = requests.get(url)

    data = r.json()

    schema = {}
    
    for i in data.get('@graph', []):
        schema_id = i.get('@id', None)
        schema[schema_id] = i 

        # Store definition
        normalized_i = schema_id.replace('schema:', '')
        db_properties_definition.post(normalized_i, i)

    # Initialize db records
    for i in schema.keys():
        
        if schema[i].get('@type', None) == 'rdf:Property':
            normalized_i = i.replace('schema:', '')
            lowered_i = normalized_i.lower()
            db_properties.post(lowered_i, normalized_i)


        elif schema[i].get('@type', None) == 'rdfs:Class':
            normalized_i = i.replace('schema:', '')
            lowered_i = normalized_i.lower()
            db_class.post(lowered_i, normalized_i)



def _download_schema_from_schema_org(record_type):
    """Download schema.org schema for a specific entity (product, person, etc)
    """

    if not record_type:
        return False

    short_record_type = record_type.replace('schema:', '')

    try:
        url = 'https://schema.org/' + short_record_type
        
        r = requests.get(url, timeout=5)

        text = r.text
        

        # Separate jsonld
        text = text.split('<script type="application/ld+json">')[1]
        text = text.split('</script>')[0]

        # Laod as json object
        new_s = json.loads(text)
        

        # store in dict

        record = {}
        for i in new_s['@graph']:
            record_id = i.get('@id', None)
            record_id = record_id.replace('schema:', '')
            record[record_id] = i
        
        db_schemas.post(record_type, record)
        
        

        return True

    except Exception as e:
        print(e)
        return False





    