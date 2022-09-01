import os
from typing import Union
from abc import ABC, abstractmethod
from framework.framework_utils.env_reader import EnvVarReader
from framework.interface.api_interface import AbstractAPI

from framework.framework_utils.code_utils import get_authentication_variable, get_api_config_variable, clean_api_name_string
from framework.framework_utils.string_utils import var_name_from_name_str
from framework.exception_handling import no_none_values


# Base Class
class AuthenticationBase(ABC):

    @abstractmethod
    def autherise_object(self, implemented_api: AbstractAPI) -> AbstractAPI:
        """getter for the autherised object"""


# Concrete Classes
class BearerOAuth(AuthenticationBase):

    def __init__(self, authentication_token_name) -> None:
        self._authentication_token_name = authentication_token_name

    def autherise_object(self, implemented_api: AbstractAPI) -> AbstractAPI:
        """Returns an object with the correct authentication bearer token."""
        header_oath = implemented_api.header  # Copy to make sure the token isn't added to the header attribute
        header_oath["Authorization"] = "Bearer {}".format(EnvVarReader().get_value(variable_name=self._authentication_token_name))
        implemented_api.header = header_oath
        return implemented_api


class ApiKeyHeaderAuth(AuthenticationBase):

    def __init__(self, authentication_token_name: str) -> None:
        self._authentication_token_name = authentication_token_name     

    def get_authed_header(self, header: dict) -> dict:
        """Returns a header with the correct authentication key, val pair."""
        header_auth = header.copy()
        header_auth["X-CMC_PRO_API_KEY"] = get_authentication_variable(variable_name=self.authentication_token_name)
        return header_auth


class ApiKeyUrlAuth(AuthenticationBase):

    def __init__(self, authentication_token_name) -> None:
        self._authentication_token_name = authentication_token_name

    # def autherise_object(self, input_object: AbstractAPI) -> AbstractAPI:
    #     _base_url = input_object.url
    #     auth_extention = os.getenv('API_ENDPOINTS_API_KEY_PLACEHOLDER') + "=" + os.getenv(self._authentication_token_name)
    #     input_object.url = _base_url + "?" + auth_extention
    #     return input_object
    def autherise_object(self, input_object: AbstractAPI) -> AbstractAPI:
        input_object.query_parameters[os.getenv('API_ENDPOINTS_API_KEY_PLACEHOLDER')] = os.getenv(self._authentication_token_name)
        return input_object


class RapidApiAuth(AuthenticationBase):

    def __init__(self, authentication_token_name: str) -> None:
        self.authentication_token_name = authentication_token_name

    def get_authed_header(self, header: dict) -> dict:
        work_header = header.copy()
        work_header["X-RapidAPI-Key"] = get_authentication_variable(variable_name=self.authentication_token_name)
        return work_header




# Director
class Authenticator:

    def __init__(self, implemented_api: AbstractAPI) -> None:
        self.__authentication_object: AuthenticationBase = self.__get_authentication_object(implemented_api)
    
    def autherise_object(self, input_object: AbstractAPI) -> AbstractAPI:
        return self.__authentication_object.autherise_object(input_object)
        

    def __get_authentication_object(self, implemented_api: AbstractAPI) -> AuthenticationBase:
        """Secret method to set the authentication object based on the authentication type specified in the implemented api"""
        # get specific authentication object
        if implemented_api.authentication_type == 'rapid_api':
            # get name of env key var of the api
            __key_var_name = var_name_from_name_str(name_sting=implemented_api.name, usage='api-key')
            return RapidApiAuth(__key_var_name)
        elif implemented_api.authentication_type == 'bearer_token':
            # get name of env key var of the api
            __key_var_name = var_name_from_name_str(name_sting=implemented_api.name, usage='bearer-token')
            return BearerOAuth(__key_var_name)
