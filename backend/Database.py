import os
from typing import Any
import pandas as pd
import sqlalchemy

class Database:
    def __init__(self, database_path: str, table_name: str):
        self.table_name = table_name
        self.database_path = database_path

        self.engine = sqlalchemy.create_engine(f'sqlite:///{self.database_path}', echo=False)
        self.connection = self.engine.connect()

    def __enter__(self):

        return self


    def exec_query(self, query):
        execute = self.connection.execute(query)

        return execute.fetchall()

    def __exit__(self, exc_type, exc_value, tb):
        self.connection.close()


