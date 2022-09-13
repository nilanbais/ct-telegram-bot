"""
API interface to implement when building an implementation for a specific api. 
"""

from abc import ABC, abstractmethod


class AbstractAPI(ABC):

    @property
    @abstractmethod
    def name(self):
        """Name of the implemented api (for referenceses).
            Set as type: str.
        """
        ...
    
    @property
    @abstractmethod
    def authentication_type(self):
        """The authentication type used with the implemented api.
            Set as type: str.
        """
        ...
    
    @property
    @abstractmethod
    def header(self):
        """The header used in the request made to the implemented api
            Set as type: dict.
        """
        ...
    
    @property
    @abstractmethod
    def url(self):
        """The url used in the request made to the implemented api.
            Set as type: str.
        """
        ...
    
    @property
    @abstractmethod
    def query_parameters(self):
        """The query parameters used in the request made to the implemented api
            Set as type: dict."""
        ...
    
    @abstractmethod
    def prepare_request_objects(self, endpoint: str, header_kwargs: dict, query_parameters_kwargs: dict, **kwargs) -> None:
        """Method to prepare the request objects. This method needs to be called at initialization"""
        ...