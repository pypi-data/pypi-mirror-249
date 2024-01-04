from functools import lru_cache

from . import _datatype_country 
from . import _datatype_state
from . import _datatype_zipcode

from i18naddress import InvalidAddressError, normalize_address

def validate(data):

    new_value = normalize(data)

    if new_value: 
        return True
    else:
        return False


    


def normalize(data):

    if not isinstance(data, dict):
        return None
        
    streetAddress = data.get('streetAddress', None)
    addressLocality = data.get('addressLocality', None)
    addressRegion = data.get('addressRegion', None)
    postalCode = data.get('postalCode', None)
    addressCountry = data.get('addressCountry', None)
    
    
    # Normalize country
    normalized_addressCountry = _datatype_country.normalize(addressCountry)

    # Normalize state
    normalized_addressRegion = _datatype_state.normalize(normalized_addressCountry, addressRegion)

    # Normalize zipcode
    normalized_postalCode = _datatype_zipcode.normalize(normalized_addressCountry, postalCode)

    
    # Normalize structure
    
    address = normalize_address({
        'country_code': normalized_addressCountry,
        'country_area': normalized_addressRegion,
        'city': addressLocality,
        'postal_code': normalized_postalCode,
        'street_address': streetAddress})

    
    new_record = {
        'streetAddress': address.get('street_address', None),
        'addressLocality': address.get('city', None),
        'addressRegion': address.get('country_area', None),
        'addressCountry': address.get('country_code', None),
        'postalCode': address.get('postal_code', None),
    }

    return new_record