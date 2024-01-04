from functools import lru_cache


def validate(country_code, postal_code):

    new_value = normalize(country_code, postal_code)

    if new_value: 
        return True
    else:
        return False




@lru_cache(maxsize=32)
def normalize(country_code, postal_code):


    if not isinstance(country_code, str):
        return None

    if not isinstance(postal_code, str):
        return None
    
    if country_code == 'CA':
        if postal_code[3] != ' ':
            postal_code = postal_code[:3] + ' ' + postal_code[3:]

    
    return postal_code