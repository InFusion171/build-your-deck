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
            'card_1': 'CARD_1',
            'card_2': 'CARD_2',
            'card_3': 'CARD_3',
            'card_4': 'CARD_4',
            'card_5': 'CARD_5',
            'card_6': 'CARD_6',
            'card_7': 'CARD_7',
            'card_8': 'CARD_8',
            'tower_troop': 'TOWER_TROOP',
            'play_date': 'PLAY_DATE',
            'won_count': 'WON_COUNT',
            'lost_count': 'LOST_COUNT'
        }

        self.create_table()

        
    def create_table(self):
        self.metadata = sql.MetaData()

        self.decks_table = sql.Table(self.table_name, self.metadata,
                                    sql.Column(self.column_names['deck_id'], sql.CHAR(12), primary_key=True),
                                    sql.Column(self.column_names['card_1_evo'], sql.Integer(), nullable=True),
                                    sql.Column(self.column_names['card_2_evo'], sql.Integer(), nullable=True),
                                    sql.Column(self.column_names['card_1'], sql.Integer(), nullable=True),
                                    sql.Column(self.column_names['card_2'], sql.Integer(), nullable=True),
                                    sql.Column(self.column_names['card_3'], sql.Integer(), nullable=False),
                                    sql.Column(self.column_names['card_4'], sql.Integer(), nullable=False),
                                    sql.Column(self.column_names['card_5'], sql.Integer(), nullable=False),
                                    sql.Column(self.column_names['card_6'], sql.Integer(), nullable=False),
                                    sql.Column(self.column_names['card_7'], sql.Integer(), nullable=False),
                                    sql.Column(self.column_names['card_8'], sql.Integer(), nullable=False),
                                    sql.Column(self.column_names['tower_troop'], sql.Integer(), nullable=False),
                                    sql.Column(self.column_names['play_date'], sql.String(), nullable=False),
                                    sql.Column(self.column_names['won_count'], sql.INTEGER(), nullable=False),
                                    sql.Column(self.column_names['lost_count'], sql.INTEGER(), nullable=False),
                                    )
        
        self.metadata.create_all(self.engine)
        
    def add_decks(self, database: Database, decks: dict[int, Deck]):
        if decks is None:
            return

        transaction = database.connection.begin()

        for id, deck in decks.items():
            build_db_deck = deck.build_deck_for_db(self.column_names)

            if build_db_deck is None:
                continue

            if self.deck_id_exists(database, id):
                self.update_play_date(database, id, build_db_deck)
                self.update_won_lost_match_counter(database, id, build_db_deck)
            else:
                self.insert(database, build_db_deck)
        
        transaction.commit()

    def update_won_lost_match_counter(self, database: Database, deck_id: str, updated_deck_row: dict):
        column_won_count = self.column_names['won_count']
        column_lost_count = self.column_names['lost_count']

        database.connection.execute(
            self.decks_table.update().
            where(self.decks_table.c[self.column_names['deck_id']] == deck_id).
            values({
                column_won_count: self.decks_table.c[column_won_count] + 
                    updated_deck_row[column_won_count],

                column_lost_count: self.decks_table.c[column_lost_count] + 
                    updated_deck_row[column_lost_count]
            })
        )

    def deck_id_exists(self, database: Database, deck_id):
        exists = database.connection.execute(
            sql.select(self.decks_table.c[self.column_names['deck_id']]).
                where(self.decks_table.c[self.column_names['deck_id']] == deck_id)
        ).fetchone() 

        return exists != None

    def update_play_date(self, database: Database, deck_id: str, updated_deck_row: dict):
        database.connection.execute(
            self.decks_table.update().
            where(self.decks_table.c[self.column_names['deck_id']] == deck_id).
            values({
                self.column_names['play_date']: updated_deck_row[self.column_names['play_date']]
                })
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