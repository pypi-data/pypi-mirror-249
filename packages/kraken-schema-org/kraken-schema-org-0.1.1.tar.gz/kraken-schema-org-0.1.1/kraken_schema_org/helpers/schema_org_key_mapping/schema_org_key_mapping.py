
from functools import lru_cache
from unidecode import unidecode


@lru_cache(maxsize=32)
def get_key(key):
    """Given a key, returns its closest equivalent within schema.org
    """
    new_key = key
    new_key = new_key.lower()
    new_key = new_key.strip()
    new_key = new_key.replace('-', ' ')
    new_key = new_key.replace('.', ' ')
    new_key = new_key.replace('  ', ' ')
    new_key = unidecode(new_key)

    mappings = _get_mappings()

    return mappings.get(new_key, None)



def _get_mappings(language = 'EN-US'):
    
    
    record = {

        "given name": "givenName",
        "givenname": "givenName",
        "family name": "familyName",
        "familyname": "familyName",
        "first name": "givenName",
        "last name": "familyName",
        "street": "streetAddress",
        "city": "addressLocality",
        "province": "addressRegion",
        "state": "addressRegion",
        "address": "streetAddress",
        "postalcode": "postalCode",
        "postal code": "postalCode",
        "zipcode": "postalCode",
        "zip code": "postalCode",
        "country": "addressCountry",
        "po box": "postOfficeBoxNumber",
        "pobox": "postOfficeBoxNumber",
        "legal name": "legalName",
        "legalname": "legalName",
        "prenom": "givenName",
        "nom": "familyName",
        "nom de famille": "familyName",
        "cell": "telephone",
        "phone": "telephone",
        "courriel": "email",
        "web site": "url",
        "website": "url"

        
    }
    return record

