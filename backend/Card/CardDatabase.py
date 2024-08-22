from Database import Database
import pandas as pd

import sqlalchemy as sql

class CardDatabase(Database):
    def __init__(self, database_path: str, table_name: str):
        super().__init__(database_path, table_name)

        self.create_table()

    def create_table(self):
        self.metadata = sql.MetaData()

        self.card_table = sql.Table(self.table_name, self.metadata,
                                    sql.Column('CARD_ID', sql.Integer(), primary_key=True),
                                    sql.Column('CARD_NAME', sql.String(), nullable=False),
                                    sql.Column('CARD_MAX_LEVEL', sql.Integer(), nullable=False),
                                    sql.Column('CARD_MAX_EVOLUTION_LEVEL', sql.Integer(), nullable=True),
                                    sql.Column('CARD_NAME', sql.String(), nullable=False),
                                    sql.Column('CARD_ICON_ENDPOINT', sql.String(), nullable=False),
                                    sql.Column('CARD_ICON_EVOLUTION_ENDPOINT', sql.String(), nullable=True),
                                    )
        
        self.metadata.create_all(self.engine)

    def get_cards(self) -> dict:
        with CardDatabase(self.database_path, self.table_name) as database:
            results = database.exec_query(self.card_table.select())

        rows = dict()
        rows = rows | {row._asdict() for row in results}

        return rows
    
    def set_cards(self, cards: dict) -> None:
        with CardDatabase(self.database_path, self.table_name) as database:
            df = pd.DataFrame(cards)
            df.to_sql(self.table_name, database.connection, if_exists='replace', index=False)
