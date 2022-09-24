import os
from typing import Union
from abc import ABC, abstractmethod
from framework.framework_utils.env_reader import EnvVarReader
from framework.api.api_interface import AbstractAPI

from framework.framework_utils.string_utils import var_name_from_name_str


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

    def autherise_object(self, implemented_api: AbstractAPI) -> AbstractAPI:
        """Returns an object with the correct authentication bearer token."""
        header_oath = implemented_api.header  # Copy to make sure the token isn't added to the header attribute
        header_oath["X-CMC_PRO_API_KEY"] = EnvVarReader().get_value(variable_name=self._authentication_token_name)
        implemented_api.header = header_oath
        return implemented_api



class RapidApiAuth(AuthenticationBase):

    def __init__(self, authentication_token_name: str) -> None:
        self._authentication_token_name = authentication_token_name    

    def autherise_object(self, implemented_api: AbstractAPI) -> AbstractAPI:
        """Returns an object with the correct authentication bearer token."""
        header_oath = implemented_api.header  # Copy to make sure the token isn't added to the header attribute
        header_oath["X-RapidAPI-Key"] = EnvVarReader().get_value(variable_name=self._authentication_token_name)
        implemented_api.header = header_oath
        return implemented_api




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
            __key_var_name = var_name_from_name_str(name_string=implemented_api.name, usage='api-key')
            return RapidApiAuth(__key_var_name)
        elif implemented_api.authentication_type == 'bearer_token':
            # get name of env key var of the api
            __key_var_name = var_name_from_name_str(name_string=implemented_api.name, usage='bearer-token')
            return BearerOAuth(__key_var_name)
        elif implemented_api.authentication_type == 'api_key_header':
            __key_var_name = var_name_from_name_str(name_string=implemented_api.name, usage='api-key')
            return ApiKeyHeaderAuth(__key_var_name)
