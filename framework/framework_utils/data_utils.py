from typing import List

from datetime import datetime

from framework.framework_utils.env_reader import EnvVarReader


__RFC3339_format = EnvVarReader().get_value('TWITTER_API_TIME_FORMAT')
    

def get_RFC_timestamp(dt_object: datetime):
    """
    Returns a string that is a valid RFC3339 date and time notation.
    """
    return datetime.strftime(dt_object, __RFC3339_format)

def get_datetime_object(self, rfc_timestamp: str) -> datetime:
    """
    Returns a datatime object from a RFC3339 timestamp.
    """
    return datetime.strptime(rfc_timestamp, __RFC3339_format)


def list_to_string(input_list: List[str]) -> str:
    """
    Returns a string of the items in a list without any space between 
    the commas and letters
    """
    return ",".join(input_list) if len(input_list) > 0 else ""


def extend_dict_object(base_dict: dict, additional_values: dict) -> dict:
    """Helper method to merge two dicts and return the result.
    Returns: one large dict consisting of the two input dicts.        
    """
    fresh_dict = base_dict.copy()
    fresh_dict.update(additional_values)
    return fresh_dict