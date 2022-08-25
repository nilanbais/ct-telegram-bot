

from framework.interface.api_interface import AbstractAPI

class TwitterAPI(AbstractAPI):

    def __init__(self) -> None:
        self._name:str = "twitter"
        self._authentication_type:str = 'bearer_token'
        self._header = None
        self._url = None
        self._query_parameters = None

    # property getters
    @property
    def name(self) -> str:
        return self._name

    @property
    def authentication_type(self) -> str:
        return self._authentication_type

    @property
    def header(self) -> dict:
        return self._header

    @property
    def url(self):
        return self._url

    @property
    def query_parameters(self):
        return self._query_parameters

    # property setters
    @header.setter
    def header(self):
        pass

    @url.setter
    def url(self):
        pass

    @query_parameters.setter
    def query_parameters(self):
        pass

    def prepare_request_objects(self, endpoint: str, header_kwargs: dict, query_parameters_kwargs: dict) -> None:
        pass