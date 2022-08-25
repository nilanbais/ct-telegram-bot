from psycopg2.errors import DuplicateTable

from bot_framework.database import DatabaseConnection


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