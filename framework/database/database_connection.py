import os

import pymongo
from pymongo import MongoClient
from pymongo.database import Database, Collection

from framework.framework_utils.env_reader import EnvVarReader


class MongoDBConnection:
    """
    Class responsible for handling all the database connection actions. This also contains managing the 
    active database and the active collection. With that the class is also extended with functionalities
    to list the available databases and collections and to check if the given database/collection name.
    """
    def __init__(self) -> None:
        self._client: MongoClient = self._init_db_client()
        self._database: Database = self._client[EnvVarReader().get_value('DB_DEFAULT_DATABASE')]
        self._collection: Collection = None
    """
    # Connection Methods
    """
    def _init_db_client(self) -> MongoClient:
        __config = EnvVarReader()
        _client_object = pymongo.MongoClient(__config.get_value('DB_CONNECTION_STRING').format(__config.get_value('DB_ADMIN_PASSWORD'), __config.get_value('DB_ADMIN_NAME')))
        return _client_object
    # --- LET OP ---
    # ADMIN ACCOUNT WORDT IN DEVELOPMENT GEBRUIKT, MAAR MOET OMGESCHREVEN WORDEN NAAR READWRITEUSER
    @property
    def client(self) -> MongoClient:
        return self._client

    @property
    def database(self) -> Database:
        return self._database

    @database.setter
    def database(self, db_name: str) -> None:
        self._database = self._client[db_name]

    @property
    def collection(self) -> Collection:
        return self._collection

    @collection.setter
    def collection(self, coll_name: str) -> None:
        self._collection = self._database[coll_name]
