import os

import psycopg2


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