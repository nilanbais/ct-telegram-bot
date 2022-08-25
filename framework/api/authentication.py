
from typing import Union
from abc import ABC, abstractmethod
from framework.interface.api_interface import AbstractAPI

from framework.framework_utils.code_utils import get_authentication_variable, get_api_config_variable, clean_api_name_string
from framework.exception_handling import no_none_values


class AbstractAuthenticationObject(ABC):

    @abstractmethod
    def get_authed_header(self, header) -> dict:
        """Method to return an authenticated header"""


class BearerOAuth(AbstractAuthenticationObject):

    def __init__(self, authentication_token_name) -> None:
        self.authentication_token_name = authentication_token_name

    def get_authed_header(self, header: dict) -> dict:
        """Returns a header with the correct authentication bearer token."""
        header_oath = header.copy()  # Copy to make sure the token isn't added to the header attribute
        header_oath["Authorization"] = "Bearer {}".format(get_authentication_variable(variable_name=self.authentication_token_name))
        return header_oath


class ApiKeyAuth(AbstractAuthenticationObject):

    def __init__(self, authentication_token_name) -> None:
        self.authentication_token_name = authentication_token_name

    def get_authed_header(self, header: dict) -> dict:
        """Returns a header with the correct authentication key, val pair."""
        header_auth = header.copy()
        header_auth["X-CMC_PRO_API_KEY"] = get_authentication_variable(variable_name=self.authentication_token_name)
        return header_auth


class RapidApiAuth(AbstractAuthenticationObject):

    def __init__(self, authentication_token_name: str) -> None:
        self.authentication_token_name = authentication_token_name

    def get_authed_header(self, header: dict) -> dict:
        work_header = header.copy()
        work_header["X-RapidAPI-Key"] = get_authentication_variable(variable_name=self.authentication_token_name)
        return work_header


class Authenticator:

    def __init__(self, implemented_api: AbstractAPI) -> None:
        self.__authentication_object: AbstractAuthenticationObject = self.__get_auth_object(implemented_api)

    def get_authorised_header(self, header: dict) -> dict:
        """Method to auterise the header.
            Returns dict with the correct autherization, based on the needed autherisation.
        """
        authed_header = self.__authentication_object.get_authed_header(header)
        return authed_header

    def __get_auth_object(self, implemented_api: AbstractAPI) -> AbstractAuthenticationObject:
        """ """
        # check if the value is not None
        no_none_values(auth_type=implemented_api.authentication_type)
        # get name of env key var of the api
        __key_var_name = clean_api_name_string(name_sting=implemented_api.name, usage='api-key')
        # get specific authentication object
        if implemented_api.authentication_type == 'rapid_api':
            return RapidApiAuth(__key_var_name)
        elif implemented_api.authentication_type == 'bearer_token':
            return BearerOAuth(__key_var_name)