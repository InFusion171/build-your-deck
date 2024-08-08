import os
from typing import Any
import pandas as pd
import sqlite3

class Database:
    def __init__(self, database_path: str, table_name: str):
        self.table_name = table_name
        self.database_path = database_path

        if not self.check_database_exists():
            print(f'Database: {self.database_path} dont exists')
            print('Created new Database')

    def open_db_connection(self):
        self.db_conn = sqlite3.connect(self.database_path)
        self.cursor = self.db_conn.cursor()

    def check_database_exists(self) -> bool:
        if(os.path.isfile(self.database_path)):
            self.open_db_connection()
            return True

        self.open_db_connection()

        return False

    def exec_query(self, query: str) -> list[Any]:
        self.cursor.execute(query)

        return self.cursor.fetchall()

    def __del__(self):
        self.db_conn.close()
        self.cursor.close()


