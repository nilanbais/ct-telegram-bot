from typing import List
from psycopg2.errors import DuplicateTable

from pymongo.database import Database, Collection

from framework.database import DatabaseConnection, MongoDBConnection


class DatabaseCursor:

    def __init__(self, connector_object: DatabaseConnection) -> None:
        self.connector = connector_object

    def query_db(self, query_string: str):
        """Method to standardise the process of querying a database.
            Returns the whole result of the query.
        """
        with self.connector.connect as conn:
            cursor = conn.cursor()
            cursor.execute(query=query_string)
            result = cursor.fetchall()
        
        return result
    
    def create(self, query_string: str) -> None:
        """
        """
        with self.connector.connect as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query=query_string)
            except DuplicateTable as error:
                print(f"Skipping query. {str.capitalize(error)}")


class MongoDBCursor:

    def __init__(self, connector_object: MongoDBConnection) -> None:
        self._connector = connector_object

    @property
    def database(self):
        return self._connector.database.name

    @database.setter
    def database(self, db_name) -> None:
        self._connector.database = db_name

    @property
    def collection(self):
        return self._connector.collection.name

    @database.setter
    def collection(self, coll_name) -> None:
        self._connector.collection = coll_name

    def _prepare_crud_ops(self, database_name:str = None, collection_name:str = None) -> None:
        """Method to replce the set-if-not-None rows"""
        if database_name is not None:
            self.database = database_name

        if collection_name is not None:
            self.collection = collection_name

    def get_database_list(self) -> list:
        """Returns a list of the available collections in the active database.
        """
        return self._connector.client.list_database_names()

    def get_collection_list(self, database_name:str = None) -> list:
        self._prepare_crud_ops(database_name)
        
        return self._connector.database.list_collection_names()

    def insert_one(self, document: dict, database_name:str = None, collection_name:str = None) -> None:
        """Checks if the given database and collection are the active ones (if specified).
        Inserts a new document into the active or specified collection.
        """
        self._prepare_crud_ops(database_name, collection_name)

        self._connector.collection.insert_one(document)

    def insert_many(self, documents: List[dict], database_name:str = None, collection_name:str = None) -> None:
        """Checks if the given database and collection are the active ones (if specified).
        Inserts a new document into the active or specified collection.
        """
        self._prepare_crud_ops(database_name, collection_name)

        self._connector.collection.insert_many(documents)

    def select_one(self, query_document: dict, database_name:str = None, collection_name:str = None) -> None:
        """
        
        """
        self._prepare_crud_ops(database_name, collection_name)
        query_result = self._connector.collection.find_one(query_document)
        return query_result

    def select_many(self, query_documents: List[dict], database_name:str = None, collection_name:str = None) -> None:
        """
        
        """
        self._prepare_crud_ops(database_name, collection_name)
        query_result = self._connector.collection.find(query_documents)
        return query_result