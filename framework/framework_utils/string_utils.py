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