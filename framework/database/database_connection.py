import os

import pymongo
from pymongo import MongoClient
from pymongo.database import Database, Collection

import psycopg2

from framework.framework_utils.env_reader import EnvVarReader

class DatabaseConnection():

    def __init__(self, user: str = None, password: str = None, host: str = None, port: int = None, dbname: str = None, use_env_file: bool = False) -> None:
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.dbname = dbname
        self.use_env_file = use_env_file

    @property
    def connect(self):
        """Property method that sets up a connection with the database"""
        if self.use_env_file:
            self.__set_attrs_from_env_file()

        connection_object = psycopg2.connect(
            user=self.user, 
            password=self.password,
            host=self.host,
            port=self.port,
            dbname=self.dbname
        )
        return connection_object

    def __set_attrs_from_env_file(self) -> None:
        """Method to set class attributes when given a db environmental variable file.
            ALL ENV FILE HAVE TO BE GATHERED IN THE ENV FOLDER.
            A db.env file has to have the following variables:
                -   DB_USER
                -   DB_PASSWORD
                -   DB_HOST  -> in a docker app this will be the conatiner name in which the db is hosted
                -   DB_PORT
                -   DB_NAME
        """
        self.user = os.getenv('DB_USER', None)
        self.password = os.getenv('DB_PASSWORD', None)
        self.host = os.getenv('DB_HOST', None)
        self.port = os.getenv('DB_PORT', None)
        self.dbname = os.getenv('DB_NAME', None)


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
