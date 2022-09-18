

from typing import Optional


def no_none_values(**kwargs) -> Optional[str]:
    """ """
    _input = kwargs
    for key, value in _input.items():
        if value is None:
            raise ValueError(f"{key} is parsed with value 'None'. 'None' as a value is not allowed. ")

if __name__ == '__main__':
    x = None
    no_none_values(x=x)