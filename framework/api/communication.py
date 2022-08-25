"""
Objects related to the general communication between a system and an api
"""
import requests

from framework.api.authentication import Authenticator
from framework.api.exceptions import APIExceptions
from framework.interface.api_interface import AbstractAPI


class APICommunicator:

    def __init__(self, implemented_api: AbstractAPI) -> None:
        self.api = implemented_api
        self.__auth_object = Authenticator(implemented_api)

    def connect_to_endpoint(self, endpoint, header_kwargs, query_parameters_kwargs) -> dict:
        """Method to connect to the endpoint of the implemented api"""

        self.api.prepare_request_objects(endpoint, header_kwargs, query_parameters_kwargs)
        
        APIExceptions().raise_request_exception(header=self.api.header, url=self.api.url, query_parameters=self.api.query_parameters)

        response = requests.request("GET", 
                                    url=self.api.url, 
                                    headers=self.__auth_object.get_authorised_header(self.api.header), 
                                    params=self.api.query_parameters)

        APIExceptions().check_response_status(response)

        return response.json()

    # property getters
    @property
    def name(self) -> str:
        return self.api.name

    @property
    def authentication_type(self) -> str:
        return self.api.authentication_type

    @property
    def header(self) -> dict:
        return self.api.header

    @property
    def url(self):
        return self.api.url

    @property
    def query_parameters(self):
        return self.api.query_parameters