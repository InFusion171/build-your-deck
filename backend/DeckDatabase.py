from collections import defaultdict
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
                                    sql.Column('CARD_1_EVO', sql.Integer(), nullable=False),
                                    sql.Column('CARD_2_EVO', sql.Integer(), nullable=False),
                                    sql.Column('CARD_3', sql.Integer(), nullable=False),
                                    sql.Column('CARD_4', sql.Integer(), nullable=False),
                                    sql.Column('CARD_5', sql.Integer(), nullable=False),
                                    sql.Column('CARD_6', sql.Integer(), nullable=False),
                                    sql.Column('CARD_7', sql.Integer(), nullable=False),
                                    sql.Column('CARD_8', sql.Integer(), nullable=False)
                                    )
        
        self.metadata.create_all(self.engine)
        
    def add_decks(self, decks: dict[int, Deck]):
        decks_table = defaultdict(list)

        for id, deck in decks.items():
            d = deck.get_deck()

            decks_table['DECK_ID'].append(id)
            decks_table['CARD_1_EVO'].append(d[0])
            decks_table['CARD_2_EVO'].append(d[1])
            decks_table['CARD_3'].append(d[2])
            decks_table['CARD_4'].append(d[3])
            decks_table['CARD_5'].append(d[4])
            decks_table['CARD_6'].append(d[5])
            decks_table['CARD_7'].append(d[6])
            decks_table['CARD_8'].append(d[7])


        df = pd.DataFrame(decks_table)

        with DeckDatabase(self.database_path, self.table_name) as database:
            df.to_sql(self.table_name, con=database, if_exists='append')