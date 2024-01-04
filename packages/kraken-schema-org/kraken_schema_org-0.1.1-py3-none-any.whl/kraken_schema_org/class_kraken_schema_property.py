
    
import copy
from kraken_schema_org.helpers import json
import os
import pkg_resources
from kraken_schema_org import kraken_schema_org as k
"""
Notes:
To access files in data directory, use:
new_path = pkg_resources.resource_filename('kraken_schema_org', old_path)

"""



class Schema_property:

    def __init__(self, property_name=None, value=None):
        """
        """
        self._property_name = property_name
        self._property_schema = {}
        self._value = value

        
    
    def get_localized(self, language='EN-US'):
        """
        """
        return k.get_localized_key(self._property_name, language)

    
    @property
    def json_types(self):
        """returns the json type (string, object, array, etc)
        Ref: https://json-schema.org/understanding-json-schema/reference/type
        """
        return k.key_get_json_types(self._property_name)

    @property
    def jsonld_types(self):
        """returns the json type (string, object, array, etc)
        Ref: https://json-schema.org/understanding-json-schema/reference/type
        """
        return k.key_get_jsonld_types(self._property_name)
        
    @property
    def python_types(self):
        """returns the pyton type (str, list, dict, datetime, float, int)
        """
        return k.key_get_python_types(self._property_name)

    def html_types(self):
        """returns the html type 
        Ref: https://www.w3schools.com/html/html_form_input_types.asp
        """
        return k.key_get_html_types(self._property_name)
        