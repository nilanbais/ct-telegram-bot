"""https://developer.twitter.com/en/docs/twitter-api/tweets/lookup/introduction
"""
from framework.framework_utils.env_reader import EnvVarReader
from framework.api.api_interface import AbstractAPI
from framework.framework_utils.string_utils import CustomFormatter, var_name_from_name_str
from framework.framework_utils.file_reader import read_json_file


class TwitterAPI(AbstractAPI):

    def __init__(self) -> None:
        self._name:str = "twitter"
        self._authentication_type:str = 'bearer_token'
        self._header:dict = {}
        self._url:str = ""
        self._query_parameters:dict = {}

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
    def url(self) -> str:
        return self._url

    @property
    def query_parameters(self) -> dict:
        return self._query_parameters

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


    def prepare_request_objects(self, endpoint: str, header_kwargs: dict, query_parameters_kwargs: dict, **kwargs) -> None:

        self.url = self._get_url(endpoint)
        if "user_id" in kwargs.keys():
            self.url = CustomFormatter().format(self.url, **{"USER_ID": kwargs['user_id']})
        else:
            self.url.format(self._get_user_id())

        self.header = header_kwargs
        self.query_parameters = query_parameters_kwargs

    def _get_url(self, endpoint: str) -> str:
        """Method to extract the url related to the given endpoint of the api"""
        API_ENDPOINT_FILE:str = EnvVarReader().get_value('API_ENDPOINTS_FILE')
        endpoint_base_url:str = read_json_file(json_file=API_ENDPOINT_FILE)[var_name_from_name_str(self.name, usage='endpoints')][endpoint]
        return endpoint_base_url  # Deleted formatting of base_user_id, need the same urls with other user_ids to look up their tweets

    def _get_user_id(self) -> str:
        TWITTER_USER_ID:str = EnvVarReader().get_value("TWITTER_USER_ID")
        return TWITTER_USER_ID
