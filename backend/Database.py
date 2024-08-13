import os
from typing import Any
import pandas as pd
import sqlite3

class Database:
    def __init__(self, database_path: str, table_name: str):
        self.table_name = table_name
        self.database_path = database_path
        self.connection = None
        self.cursor = None

    def create_connection(self):
        if not self.database_exists():
            print(f'{self.database_path} dont exist. Will create a new DB')

        self.connection = sqlite3.connect(self.database_path)
        self.cursor = self.connection.cursor()

    def __enter__(self):
        if not self.database_exists():
            print(f'{self.database_path} dont exist. Will create a new DB')

        self.connection = sqlite3.connect(self.database_path)
        self.cursor = self.connection.cursor()

        return self, self.database_exists()

    def database_exists(self) -> bool:
        return os.path.isfile(self.database_path)


    def exec_query(self, query: str) -> list[Any]:
        if self.cursor is None:
            print('Need to open the Database connection before executing the query')
            return None

        self.cursor.execute(query)

        return self.cursor.fetchall()

    def __exit__(self):
        self.cursor.close()
        self.connection.close()


