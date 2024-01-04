#from kraken_schema_org.class_kraken_schema_org import Schema_org

from kraken_schema_org.helpers import schema_org_website_data as w
from kraken_schema_org.helpers import schema_org_normalizer
from kraken_schema_org.helpers import schema_org_to_json_schema as j
from kraken_schema_org.helpers import schema_org_name
from kraken_schema_org.helpers import kraken_record_id
from kraken_schema_org.helpers import schema_org_sample_data
from kraken_schema_org.helpers import schema_org_localize
from kraken_schema_org.helpers import schema_org_key_mapping
from kraken_schema_org.helpers import schema_org_summary
from kraken_schema_org.helpers import schema_org_normalizer

from kraken_schema_org.helpers import schema_org_types




"""
Legacy methods (for backward compatibility)
"""
def normalize_type(record_type):
    """Return normalized record_type
    """
    return w.get_class(record_type)
    

def normalize_key(key):
    """Return normalized key (property)
    """
    return w.get_property(key)


def normalize_record(record):
    """Return a record fully normalized (keys and values)
    """
    return get_normalized_record(record)

def normalize_value(record_type, key, value, default=None, strict=True):

    return schema_org_normalizer.normalize_value(key, value)
    

def get_datatype(record_type, key):
    """Get datatype for given key
    """
    return key_get_jsonld_types(key)



"""
Class methods
"""

def get_class(record_type):
    return w.get_class(record_type)

def get_schema(record_type):
    """Returns schema for record_type
    """
    return w.get_schema(record_type)


def get_json_schema(record_type):
    """Given a record_type, returns the json schema
    """
    return j.get_json_schema(record_type)

def get_data(record_type):
    """Get sample record for given record_type
    """
    return schema_org_sample_data.get_sample_data(record_type)
    
def get_summary_keys(record_type):
    """Get minimum keys required for display
    """
    return schema_org_summary.get_summary_keys(record_type)


"""
Property methods
"""

def get_key(key):
    """Returns formatted key (attribute)
    """
    return w.get_property(key)

def get_keys(record_type):
    """Return all keys (properties) for a record_type
    """
    record_type = get_record_type(record_type)
    return w.get_keys(record_type)
    

def key_get_jsonld_types(key):
    """Returns jsonld schema type for a given key
    """
    key = get_key(key)
    return schema_org_types.get_jsonld_types(key) 

def key_get_json_types(key):
    """Returns json schema type for a given key
    """
    key = get_key(key)
    return schema_org_types.get_json_types(key) 

def key_get_python_types(key):
    """Returns json schema type for a given key
    """
    key = get_key(key)
    return schema_org_types.get_python_types(key) 

def key_get_html_types(key):
    """Returns html type
    Ref: https://www.w3schools.com/html/html_form_input_types.asp
    """
    key = get_key(key)
    return schema_org_types.get_html_types(key)

def get_localized_key(key, language='EN-US'):
    """Returns usual key name for a given language (ex givenNanme == First name)
    """
    return schema_org_localize.get_localized_attribute(key, language)

def convert_key(key):
    """Returns official key from given key (ex: last name -> familyName)
    """
    return schema_org_key_mapping.get_key(key)

def get_key_definition(key):
    """
    """
    return w.get_property_definition(key)

def get_normalized_value(key, value):
    return schema_org_normalizer.normalize_value(key, value)


"""
Record based methods
"""
def get_record_type(record):
    """Given a record, return formatted record_type 
    """
    record_type = record if not isinstance(record, dict) else record.get('@type', None)
    return w.get_class(record_type)
    
def get_record_id(record):
    """Given a record, return it's record_id based on conventions
    """
    return kraken_record_id.get_record_id(record)

def get_record_name(record):
    """Given a record, return it's display name based on conventions
    """
    return schema_org_name.get_name(record)


def get_normalized_record(record):
    """Returns a fully normalized record
    """
    return schema_org_normalizer.normalize(record)

def get_summary_record(record):
    """returns localized record based on language
    """
    return schema_org_summary.get_summary_record(record)

def get_localized_record(record, language='EN-US'):
    """returns localized record based on language
    """
    return schema_org_localize.localize_record(record, language)


