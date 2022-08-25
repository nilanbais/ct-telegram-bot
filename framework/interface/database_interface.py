
from typing import Protocol


class DBInterface(Protocol):

    def update_record():
        ...
    
    def query_db(self, query: str):
        ...

    def update_many(self):
        ...