"""
All utility type functionalities collected in one place
"""
from datetime import datetime
import os
from typing import Union

import dotenv


date_format = '%Y-%m-%d'


# Get absolute path of project root
def get_abs_project_root() -> str:
    """ """
    RETURN_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    while not RETURN_PATH.endswith('bot'):  # todo: 'bot' vervangen voor configuratie waarde
        RETURN_PATH = os.path.abspath(os.path.join(RETURN_PATH, os.pardir))

    return RETURN_PATH


def load_project_config_env() -> None:
    """ """
    dotenv.load_dotenv(dotenv_path=os.path.join(get_abs_project_root(), 'config.env'))


def get_api_config_variable(variable_name: str) -> str:
    """ """
    __result = dotenv.dotenv_values(dotenv_path=os.path.join(get_abs_project_root(), 'env', 'api_config.env'))
    return __result[variable_name]


def get_authentication_variable(variable_name: str) -> str:
    """Function to retrieve variables from authentication.env. Use this function to prefent
       authentication variables to be exposed through the common envirnmental variables.
        Returns a single string value.
    """
    __result = dotenv.dotenv_values(dotenv_path=os.path.join(get_abs_project_root(), 'env', 'authentication.env'))
    return __result[variable_name]

def get_db_connection_variables(variable_name: str = None) -> Union[dict, str]:
    """Function to retrieve the db connection variables as a whole or one signle value."""
    __result = dotenv.dotenv_values(dotenv_path=os.path.join(get_abs_project_root(), 'env', 'db.env'))
    if variable_name is None:
        return __result
    return __result[variable_name]

def clean_api_name_string(name_sting: str, usage: str) -> str:
    """function to return clean api string.
        usage specifies for which goal the string needs to be cleaned.
    """
    __string = str.upper(name_sting)
    __string = __string.replace("_", "")
    if usage == 'authenticatation':
        return __string + "_AUTH_TYPE"
    elif usage == 'api-key':
        return __string + "API_KEY"
    elif usage == 'api-host':
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