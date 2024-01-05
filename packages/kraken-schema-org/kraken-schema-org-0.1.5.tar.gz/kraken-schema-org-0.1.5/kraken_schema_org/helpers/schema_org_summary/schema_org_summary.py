


def get_summary_record(record):
    """Transform a record into a summary record
    """
    if isinstance(record, dict):
        record_type = record.get('@type', None)
        summary_keys = get_summary_keys(record_type)
        
        new_record = {}
        for k, v in record.items():
            if k in summary_keys or not record_type:
                new_record[k] = get_summary_record(v)
                    
        return new_record

    elif isinstance(record, list):
        return [get_summary_record(x) for x in record]
        
    else:
        return record
        

def get_summary_keys(record_type):
    """Given a record_type, returns the minimum keys required
    """

    keys = ['@type', '@id', 'name', 'url']

    keys_db = _summary_db()

    keys += keys_db.get(record_type, [])

    return keys




def _summary_db():
    """
    """

   
    
    record ={
        'address': [
            'name',
            'streetAddress',
            'addressLocality',
            'addressRegion',
            'addressCountry',
            'postalCode'
        ],
        'person':[
            'givenName',
            'familyName',
            'email',
            'telephone',
            'address',
            'jobTitle',
            'worksFor'
        ],
        'organization': [
            'address'
        ]
    }
    return record

    

