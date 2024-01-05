"""
Methods to nornalize schema.org records

Converts a record into a standardized record using proper schema.org terms.

"""

import os
import copy
import datetime
import uuid


import kraken_datatype as dt 
from kraken_schema_org.helpers import schema_org_website_data as w
from kraken_schema_org.helpers import kraken_record_id
from kraken_schema_org.helpers import schema_org_types


def normalize(original_record, strict=False, parent_key=None):
    """
    """
    # Make copy of original record
    record = copy.deepcopy(original_record)
    
    if isinstance(record, list):
        return [normalize(x, strict, parent_key) for x in record]
    
    elif isinstance(record, dict):
        
        record_type = w.get_record_type(record)
        
        # Initialize new record
        new_record = {'@type': record_type, '@id': None}

        # Iterate through key/value
        for k, v in record.items():

            # Skip if @type or @id
            if k in ['@type', '@id']:
                continue

            # normalize key
            new_k = w.get_key(k)

            # Skip if new_k is None and strict, else reassigns old key
            if not new_k:
                if strict == True:
                    continue
                else:
                    new_k = k
            
            # Skip if key not in schema (if strict)
            if new_k not in w.get_keys(record_type) and strict == True:                
                continue

            # Normalize value through recursion
            new_value = normalize(v, strict, new_k)

            if not new_value:
                continue
            
            new_record[new_k] = new_value

        # generate record_id based on normalized values
        new_record['@id'] = kraken_record_id.get_record_id(new_record)

        # return

        return new_record

    else:
        # Normalize value
        v = record

        # Retrieve possible datatypes
        datatypes = schema_org_types.get_jsonld_types(parent_key)
        if not datatypes:
            if strict == True:
                print('ccc', v)
                return None
            else:
                return v
        
        # Try nromalizing base don each datatypes, keep first one that works
        best_value = None
            
        for i in datatypes:
            print('iii', i)
            if i == 'object' and best_value == None:
                best_value = v
            else:
                new_v = dt.normalize(i,v)
                best_value = new_v if new_v else best_value
            
        # If nothing returns None if strict, else returns original value
        print('bv', best_value)
        if best_value == None: 
            return None if strict == True else v
        else:
            return best_value
         




def normalize_value(key, value, strict=True):
    """Normalize value
    """


    if key in ['@type', '@id']:
        return None

    # Normalize key
    key = norm.normalize_key(key)

    if not key and strict:
        return None

    # Get datatypes
    datatypes = norm.get_datatype(record_type, key)

    # Intialize output_record value
    output_record = []

    # Cycle through possible datatypes
    for i in datatypes or []:
        result = _normalize_value(i, key, value, strict)
        if result and result not in output_record:
            output_record.append(result)

    # Convert back from list if one or None
    if len(output_record) == 1:
        output_record = output_record[0]
    elif len(output_record) == 0:
        output_record = None


    return output_record


def _normalize_value(datatype, key, value, strict=True):

    if isinstance(value, list):
        results = []
        for i in value:
            results.append(_normalize_value(datatype, key, i, strict))
        return results


    # Normalize value if also a record
    if isinstance(value, dict):
        # Normalize record if schema
        if '@type' in value.keys():
            value = get(value)

        # Return normalized record if same datatype
        if value.get('@type', None) == datatype:
            return value
        else:
            return None


    if not isinstance(value, (int, str, float)):
        return value

    # Try to normalize, if not working keep value
    try:
        result = dt.normalize(datatype, value)
    except:
        if strict:
            result = None


    return result

