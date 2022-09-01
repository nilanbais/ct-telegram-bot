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

    def connect_to_endpoint(self, endpoint: str, header_kwargs: dict = {}, query_parameters_kwargs: dict = {}) -> dict:
        """Method to connect to the endpoint of the implemented api"""
        self.api.prepare_request_objects(endpoint, header_kwargs, query_parameters_kwargs)
        autherised_object: AbstractAPI = self.__auth_object.autherise_object(self.api)

        print(f"header={autherised_object.header}, url={autherised_object.url}, query_parameters={autherised_object.query_parameters}")

        APIExceptions().raise_request_exception(header=autherised_object.header, url=autherised_object.url, query_parameters=autherised_object.query_parameters)
        
        response = requests.request("GET", 
                                    url=autherised_object.url, 
                                    headers=autherised_object.header, 
                                    params=autherised_object.query_parameters)

        APIExceptions().check_response_status(response)
        print(type(response))
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
    
    # property setters
    @header.setter
    def header(self, new_header: dict):
        self._header = new_header

    @url.setter
    def url(self, new_url: str):
        self._url = new_url

    @query_parameters.setter
    def query_parameters(self, new_query_parameters: dict):
        self._query_parameters = new_query_parameters