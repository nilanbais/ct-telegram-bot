from string import Formatter

class CustomFormatter(Formatter):
    def get_value(self, key, args, kwds):
        if isinstance(key, str):
            try:
                return kwds[key]
            except KeyError:
                return key
        else:
            return Formatter.get_value(key, args, kwds)

def var_name_from_name_str(name_sting: str, usage: str) -> str:
    """function to return clean api string.
        usage specifies for which goal the string needs to be cleaned.
    """
    __string = str.upper(name_sting)
    __string = __string.replace("-", "_").replace(" ", "_")
    if usage == 'api-key':
        return "API_KEY_" + __string
    elif usage == 'bearer-token':
        return 'API_BEARER_TOKEN_' + __string
    elif usage == 'endpoints':
        return __string

def var_name_from_name_string(name_string: str, usage: str) -> str:
    __string = str.upper(name_string)
    __string = __string.replace("-", "_").replace(" ", "_")
    match usage:
        case 'api-key':
            return "API_KEY_" + __string
        case 'bearer-token':
            return 'API_BEARER_TOKEN_' + __string
        case 'endpoints':
            return __string

        
def check_for_char(input_string: str, character: str) -> bool:
    """Function to check if a character is present in the given string.
        Returns a boolean value.
    """
    return character in input_string