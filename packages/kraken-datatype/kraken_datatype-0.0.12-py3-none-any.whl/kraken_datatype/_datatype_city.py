from functools import lru_cache


def validate(data):

    new_value = normalize(data)

    if new_value: 
        return True
    else:
        return False




@lru_cache(maxsize=32)
def normalize(data):


    if not isinstance(data, str):
        return None

    new_data = data.upper()
    

    return None