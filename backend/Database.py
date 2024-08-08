import os
from typing import Any
import pandas as pd
import sqlite3

class Database:
    def __init__(self, database_path: str, table_name: str):
        self.table_name = table_name
        self.database_path = database_path

        self.check_database_exists()

        self.db_conn = sqlite3.connect(database_path)
        self.cursor = self.db_conn.cursor()

    def check_database_exists(self) -> bool:
        if(os.path.isfile(self.database_path)):
            return True
        
        print(f'Database: {self.database_path} dont exists')

        return False

    def createTopPlayersDatabase(self, top_players: dict):
        player_list = [{'playerTag' : tag, 'elo': elo} for elo, tag in top_players.items()]

        df = pd.DataFrame(player_list)
        df.to_sql(self.table_name, self.db_conn, if_exists='replace', index=False)

    def get_locations(self):
        records = self.exec_query()

    def exec_query(self, query: str) -> list[Any]:
        self.cursor.execute(query)

        return self.cursor.fetchall()

    def __del__(self):
        self.db_conn.close()


