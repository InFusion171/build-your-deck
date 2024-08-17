from collections import defaultdict
import pandas as pd
from Database import Database
from Deck import Deck

import sqlalchemy as sql

class DeckDatabase(Database):
    def __init__(self, database_path: str, table_name: str):
        super().__init__(database_path, table_name)

        self.column_names = {
            'deck_id': 'DECK_ID',
            'card_1_evo': 'CARD_1_EVO',
            'card_2_evo': 'CARD_2_EVO',
            'card_3': 'CARD_3',
            'card_4': 'CARD_4',
            'card_5': 'CARD_5',
            'card_6': 'CARD_6',
            'card_7': 'CARD_7',
            'card_8': 'CARD_8',
            'play_date': 'PLAY_DATE'
        }

        self.create_table_if_not_exist()

        
    def create_table_if_not_exist(self):
        self.metadata = sql.MetaData()

        self.decks_table = sql.Table(self.table_name, self.metadata,
                                    sql.Column(self.column_names['deck_id'], sql.CHAR(10), primary_key=True),
                                    sql.Column(self.column_names['card_1_evo'], sql.Integer(), nullable=False),
                                    sql.Column(self.column_names['card_2_evo'], sql.Integer(), nullable=False),
                                    sql.Column(self.column_names['card_3'], sql.Integer(), nullable=False),
                                    sql.Column(self.column_names['card_4'], sql.Integer(), nullable=False),
                                    sql.Column(self.column_names['card_5'], sql.Integer(), nullable=False),
                                    sql.Column(self.column_names['card_6'], sql.Integer(), nullable=False),
                                    sql.Column(self.column_names['card_7'], sql.Integer(), nullable=False),
                                    sql.Column(self.column_names['card_8'], sql.Integer(), nullable=False),
                                    sql.Column(self.column_names['play_date'], sql.CHAR(8), nullable=False)
                                    )
        
        self.metadata.create_all(self.engine)
        
    def add_decks(self, decks: dict[int, Deck]):
        with DeckDatabase(self.database_path, self.table_name) as database:
            transaction = database.connection.begin()

            for id, deck in decks.items():
                build_db_deck = deck.build_deck_for_db()

                if self.deck_id_exists():
                    self.update_play_date(database, id, build_db_deck)
                else:
                    self.insert(database, build_db_deck)
            
            transaction.commit()

    def deck_id_exists(self, database: Database, deck_id):
        exists = database.connection.execute(
            sql.select().where(self.decks_table.c[self.column_names['deck_id']] == deck_id)
        ).fetchone() 

        return exists != None

    def update_play_date(self, database: Database, deck_id: str, updated_deck_row: dict):
        database.connection.execute(
            self.decks_table.update().
            where(self.decks_table.c[self.column_names['deck_id']] == deck_id).
            values({self.column_names['play_date']: updated_deck_row[self.column_names['play_date']]})
        )
    
    # unused
    def delete_deck_id_duplicate(self, database: Database, deck_id):
        database.connection.execute(
            self.decks_table.delete().where(self.decks_table.c[self.column_names['deck_id']] == deck_id)
        )

    def insert(self, database: Database, deck_row: dict):
        database.connection.execute(
            self.decks_table.insert().values(deck_row)
        )