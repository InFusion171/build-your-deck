from Database import Database
import pandas as pd

import sqlalchemy as sql

class CardDatabase(Database):
    database_path = ''
    table_name = ''

    @classmethod
    def setup_database_connection(cls, database_path: str, table_name: str):
        cls.database_path = database_path
        cls.table_name = table_name

    def __init__(self):
        if len(self.database_path) == 0 or len(self.table_name) == 0:
            print('You need to first call setup_database_connection') 
            return None

        super().__init__(self.database_path, self.table_name)

        self.column_names = {
            'card_id': 'CARD_ID',
            'card_name': 'CARD_NAME',
            'card_max_level': 'CARD_MAX_LEVEL',
            'card_rarity': 'CARD_RARITY',
            'card_max_evolution_level': 'CARD_MAX_EVOLUTION_LEVEL',
            'card_icon': 'CARD_ICON_ENDPOINT',
            'card_icon_evolution': 'CARD_ICON_EVOLUTION_ENDPOINT'
        }

        self.create_table()

    def create_table(self):
        self.metadata = sql.MetaData()

        self.card_table = sql.Table(self.table_name, self.metadata,
                                    sql.Column(self.column_names['card_id'], sql.Integer(), primary_key=True),
                                    sql.Column(self.column_names['card_name'], sql.String(), nullable=False),
                                    sql.Column(self.column_names['card_max_level'], sql.Integer(), nullable=False),
                                    sql.Column(self.column_names['card_rarity'], sql.String(), nullable=False),
                                    sql.Column(self.column_names['card_max_evolution_level'], sql.Integer(), nullable=True),
                                    sql.Column(self.column_names['card_icon'], sql.String(), nullable=False),
                                    sql.Column(self.column_names['card_icon_evolution'], sql.String(), nullable=True),
                                    )
        
        self.metadata.create_all(self.engine)

    def get_all_cards(self) -> list[dict]:
        with CardDatabase() as database:
            results = database.exec_query(self.card_table.select())

        return [row._asdict() for row in results]

    def get_deck_cards(self, evo_cards: list, cards: list):
        with CardDatabase() as database:
            evo_results = database.exec_query(sql.select(self.card_table). 
                                          filter(
                                              self.card_table.c[self.column_names['card_id']].in_(evo_cards)
                                          ))
            
            card_results = database.exec_query(sql.select(self.card_table). 
                                          filter(
                                              self.card_table.c[self.column_names['card_id']].in_(cards)
                                          ))

            return str([row._asdict()['CARD_NAME'] for row in evo_results] + [row._asdict()['CARD_NAME'] for row in card_results])

    
    def set_cards(self, cards: list[dict]) -> None:
        df = pd.DataFrame(cards)
        df.to_sql(self.table_name, self.engine, if_exists='replace', index=False)
