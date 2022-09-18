"""
All utility type functionalities collected in one place
"""
from datetime import datetime
import os
from typing import Union

import dotenv


date_format = '%Y-%m-%d'


def clean_api_name_string(name_sting: str, usage: str) -> str:
    """function to return clean api string.
        usage specifies for which goal the string needs to be cleaned.
    """
    __string = str.upper(name_sting)
    __string = __string.replace("_", "")
    match usage:   
        case 'authenticatation':
            return __string + "_AUTH_TYPE"
        case 'api-key':
            return __string + "API_KEY"
        case 'api-host':
            return __string + "API_HOST"


def get_date_str(input_date: datetime) -> str:
    """Returns a date string with the correct format"""
    return datetime.strftime(input_date, date_format)


def check_date_format(input_date: str, date_format: str = date_format) -> bool:
    """Checks if the input date has the correct format of '%Y-%m-%d'. """
    if isinstance(input_date, str):
        datetime.strptime(input_date, date_format)
        return True
    else:
        raise TypeError(f"Please parse your date as a sting. You parsed an object with type {type(input_date)}.")


if __name__ == '__main__':
    date = datetime(day=22, month=1, minute=6, year=1995)
    print(check_date_format(date))