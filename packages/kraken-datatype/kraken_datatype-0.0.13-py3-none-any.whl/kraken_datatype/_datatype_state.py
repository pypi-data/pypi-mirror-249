from functools import lru_cache
import pycountry



def validate(country_code, state_code):

    new_value = normalize(country_code, state_code)

    if new_value: 
        return True
    else:
        return False



@lru_cache(maxsize=32)
def normalize(country_code, state_code):
    

    if not isinstance(country_code, str):
        return None
    if not isinstance(state_code, str):
        return None
    

    code = country_code.upper() + '-' + state_code.upper()

    # Search for specific country and state code
    results = pycountry.subdivisions.get(code=code)
    if results:
        state_code = results.code
        state_code = state_code.replace(country_code, '').replace('-', '')
        return state_code


    # Else search by name
    states = pycountry.subdivisions.search_fuzzy(state_code)
    states = [x for x in states if x.country_code == country_code.upper()]

    if len(states) == 1:
        state_code = states[0].code
        state_code = state_code.replace(country_code, '').replace('-', '')
        return state_code

    return None