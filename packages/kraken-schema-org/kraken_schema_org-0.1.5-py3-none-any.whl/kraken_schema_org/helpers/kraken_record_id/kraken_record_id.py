"""
Methods to assign a record_id to a record based on conventions

"""

import uuid
from urllib.parse import urlparse



def get_record_id(record):
    """Given a record, define record_id based on standards

    website: uuid of domain
    webpage(s): uuid of url
    
    """

    # Error handling
    if not isinstance(record, dict):
        return None

    # Error handling
    record_type = record.get('@type', None)
    if not record_type:
        return None

    # Get values
    record_type = record.get('@type', None)
    record_id = record.get('@id', None)
    url = record.get('url', None)
    contentUrl = record.get('contentUrl', None)
    record_type = record_type.lower().replace('schema:', '')

    
    # IF current record_id doesn't start with "_", assume it is valid
    #if record_id and not record_id.startswith('_'):
    #    return record_id

    
    # Define id by rcord_type
    if record_type in _get_domain_elements():
        return _get_id_from_domain(url)
    
    # Define id by rcord_type
    if record_type in _get_web_elements():
        return _get_id_from_url(url)

    # Define id by rcord_type
    if record_type in _get_media_elements():
        return _get_id_from_url(contentUrl)

    # Define id by rcord_type
    if record_type in _get_address_elements():
        return _get_id_from_address(record)

    return _get_UUID()


def _get_UUID():
    """
    """
    return str(uuid.uuid4())

def _get_id_from_url(url):
    """
    """

    if not url or not isinstance(url, str):
        return None

    
    try:
        record_id = str(uuid.uuid5(uuid.NAMESPACE_URL, url))
        print('r', record_id)
        return record_id

    except Exception as e:
        print(e)
        return None


def _get_id_from_domain(url):
    """
    """
    if not url or not isinstance(url, str):
        return None

    try:
        domain = urlparse(url).netloc

        if not domain:
            return None
        
        record_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, domain))
        return record_id

    except Exception as e:
        print(e)
        return None


def _get_id_from_address(address):
    """Given an address, returns a unique uuid
    """
    if not address or not isinstance(address, dict):
        print('no address')
        return None

    streetAddress = address.get('streetAddress', None)
    addressLocality = address.get('addressLocality', None)
    addressRegion = address.get('addressRegion', None)
    addressCountry = address.get('addressCountry', None)
    postalCode = address.get('postalCode', None)

    add_comp = [streetAddress, addressLocality, addressRegion, addressCountry, postalCode]

    # Eliminate if incomplete
    for i in add_comp:
        if i is None:
            return None
        if i == '':
            return None
        if not isinstance(i, str):
            return None
        

    
    add_string = ','.join(add_comp)


    try:
        record_id = str(uuid.uuid5(uuid.NAMESPACE_X500, add_string))
        return record_id
    
    except Exception as e:
        print(e)
        return None
    
   
def _test_valid_uuid(value):
    """Test if value is a uuid
    """
    if not value:
        return None

    try:
        uuid.UUID(value)
        return True
    except ValueError:
        return None


def _get_media_elements():
    media_elements = [
        'mediaobject',
        'imageobject',
        'videoobject',
        '3dmodel',
        'ampstory',
        'audioobject',
        'datadownload',
        'legislationobject',
        'musicvideoobject',
        'textobject'
    ]
    return media_elements

def _get_web_elements():
    """
    """
    web_elements = [
        'webpage',
        'aboutpage',
        'checkoutpage',
        'collectionpage',
        'contactpage',
        'faqpage',
        'itempage',
        'medicalwebpage',
        'profilepage',
        'qapage',
        'realestatelisting',
        'searchresultspage'
    ]
    return web_elements


def _get_domain_elements():
    """
    """
    domain_elements = [
        'organization',
        'website',
        'localbusiness'
    ]
    return domain_elements


def _get_address_elements():
    address_elements = [
        'postaladdress'
    ]
    return address_elements