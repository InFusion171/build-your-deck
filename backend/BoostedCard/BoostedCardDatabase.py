from Database import Database

import sqlalchemy as sql
import pandas as pd

class BoostedCardDatabase(Database):
    database_path = ''
    table_name = ''

    @classmethod
    def setup_database_connection(cls, database_path: str, table_name: str):
        cls.database_path = database_path
        cls.table_name = table_name

    def __init__(self):
        super().__init__(self.database_path, self.table_name)

        self.create_table()

        
    def create_table(self):
        self.metadata = sql.MetaData()

        self.boosted_cards_table = sql.Table(self.table_name, self.metadata,
                                    sql.Column('CARD_ID_0', sql.Integer(), nullable=False),
                                    sql.Column('CARD_ID_1', sql.Integer(), nullable=False),
                                    sql.Column('CARD_ID_2', sql.Integer(), nullable=False),
                                    sql.Column('CARD_ID_3', sql.Integer(), nullable=False)
                                    )
        
        self.metadata.create_all(self.engine)

    def set_boosted_cards(self, cards: list[int]):
        df = pd.DataFrame({f'CARD_ID_{index}': cards[index] for index in range(len(cards))}, index=[0])

        df.to_sql(name=self.table_name, con=self.engine, if_exists='replace')

    def get_boosted_cards(self):
        cards = self.exec_query(self.boosted_cards_table.select())

        if not cards:
            return None
        
        return list(cards[0])