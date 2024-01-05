
    
import copy
from kraken_schema_org.helpers import json
import os
import pkg_resources
from kraken_schema_org import kraken_schema_org as k
from kraken_schema_org.class_kraken_schema_property import Schema_property


"""
Notes:
To access files in data directory, use:
new_path = pkg_resources.resource_filename('kraken_schema_org', old_path)

"""



class Schema_class:

    def __init__(self, class_name=None):
        """
        """
        self._class_name = class_name
        self._schema = {}

        
    def get_properties(self):
        """
        """
        return [Schema_property(x) for x in self.keys]

    
    def get_property(self, key):
        return Schema_property(key)

    
    @property
    def keys(self):
        """
        """
        k.get_keys(self._class_name)

    @property
    def summary_keys(self):
        """
        """
        k.get_keys(self._class_name)
        
    @property
    def record(self):
        """Get example record
        """
        return k.get_data(self._class_name)





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

def get_localized_record(record, language='EN-US'):
    """returns localized record based on language
    """
    return schema_org_localize.localize_record(record, language)


def normalize_record(record, strict = False):
    return s.normalize_record(record, strict)

