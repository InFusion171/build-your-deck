import pandas as pd
import sqlite3

class Database:
    def __init__(self, database_name: str, table_name: str):
        self.table_name = table_name
        self.database_name = database_name

        self.db_conn = sqlite3.connect(database_name)

    def createTopPlayersDatabase(self, top_players: dict):
        player_list = [{'playerTag' : tag, 'elo': elo} for elo, tag in top_players.items()]

        df = pd.DataFrame(player_list)
        df.to_sql(self.table_name, self.db_conn, if_exists='replace', index=False)

    def __del__(self):
        self.db_conn.close()


