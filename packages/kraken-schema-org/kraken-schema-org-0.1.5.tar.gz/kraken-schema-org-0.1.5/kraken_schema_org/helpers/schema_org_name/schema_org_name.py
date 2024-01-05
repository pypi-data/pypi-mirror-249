"""
Obtain the name of the thing based on convention if name is missing

"""





def get_name(record):
    """Obtain the name of the thing based on convention if name is missing

    """

    def get_from_list(key, record):

        if not record:
            return None

        if not isinstance(record, dict):
            return None

        value = record.get(key, None)
        if isinstance(value, list):
            if len(value) > 0:
                value = value[0]
            else:
                value = None
        return value

    record_type = get_from_list('@type', record)
    record_id = get_from_list('@id', record)
    name = get_from_list('name', record)
    url = get_from_list('url', record)


    # Return name if exists in record
    if name:
        return name

    if not record_type:
        return None

    record_type = record_type.lower()
    
    # Get name based on type
    if record_type == 'person':
        name = _get_name_from_person(record)
    if record_type == 'address':
        name = _get_name_from_address(record)

    # If empty, use url
    if not name:
        url = record.get('url', None)
        name = url

    # If empty, use type / id
    if not name:
        name = f'{record_type}/{record_id}'

    return name



def _get_name_from_person(record):
    """
    """
    def get_from_list(key, record):

        if not record:
            return None

        if not isinstance(record, dict):
            return None

        value = record.get(key, None)
        if isinstance(value, list):
            if len(value) > 0:
                value = value[0]
            else:
                value = None
        return value

    fname = get_from_list('givenName', record)
    lname = get_from_list('familyName', record)


    name = ' '.join([fname, lname])

    return name



def _get_name_from_address(record):
    """
    """
    def get_from_list(key, record):

        if not record:
            return None

        if not isinstance(record, dict):
            return None

        value = record.get(key, None)
        if isinstance(value, list):
            if len(value) > 0:
                value = value[0]
            else:
                value = None
        return value

    values = []
    for k in ['streetAddress', 'addressLocality', 'addressRegion', 'addressCountry', 'postalCode']:
        v = get_from_list(k, record)
        if v:
            values.append(v)
    name = ','.join(values)

    return name