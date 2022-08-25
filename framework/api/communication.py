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

    def connect_to_endpoint(self) -> dict:
        """Method to connect to the endpoint of the implemented api"""
        APIExceptions().raise_request_exception(header=self.api.header, url=self.api.url, query_parameters=self.api.query_parameters)
        
        response = requests.request("GET", 
                                    url=self.api.url, 
                                    headers=self.__auth_object.get_authorised_header(self.api.header), 
                                    params=self.api.query_parameters)

        APIExceptions().check_response_status(response)

        return response.json()