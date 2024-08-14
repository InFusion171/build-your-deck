import pandas as pd
from Database import Database
from Deck import Deck

import sqlalchemy as sql

class DeckDatabase(Database):
    def __init__(self, database_path: str, table_name: str):
        super().__init__(database_path, table_name)

        self.create_table_if_not_exist()

        
    def create_table_if_not_exist(self):
        self.metadata = sql.MetaData()

        self.decks_table = sql.Table(self.table_name, self.metadata,
                                    sql.Column('DECK_ID', sql.Integer(), primary_key=True),
                                    sql.Column('CARD_EVO_1', sql.Integer(), nullable=False),
                                    sql.Column('CARD_EVO_2', sql.Integer(), nullable=False),
                                    sql.Column('CARD_3', sql.Integer(), nullable=False),
                                    sql.Column('CARD_4', sql.Integer(), nullable=False),
                                    sql.Column('CARD_5', sql.Integer(), nullable=False),
                                    sql.Column('CARD_6', sql.Integer(), nullable=False),
                                    sql.Column('CARD_7', sql.Integer(), nullable=False),
                                    sql.Column('CARD_8', sql.Integer(), nullable=False)
                                    )
        
        self.metadata.create_all(self.engine)
        
    def add_decks(self, decks: dict):
        print(decks)

        deck_id = [d.__hash__() for d in decks.keys()]
        decks = [d.get_deck() for d in decks.values()]

        df = pd.DataFrame({'DECK_ID': deck_id, 'DECKS': decks})

        with DeckDatabase(self.database_path, self.table_name) as (database, _):
            df.to_sql(self.table_name, con=database, dtype={'DECK_ID': 'INTEGER PRIMARY KEY'})