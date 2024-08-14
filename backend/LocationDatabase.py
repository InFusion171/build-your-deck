from Database import Database
import pandas as pd

import sqlalchemy as sql

class LocationDatabase(Database):
    def __init__(self, database_path: str, table_name: str):
        super().__init__(database_path, table_name)

        self.create_table_if_not_exist()

    def create_table_if_not_exist(self):
        self.metadata = sql.MetaData()

        self.location_table = sql.Table(self.table_name, self.metadata,
                                    sql.Column('LOCATION_ID', sql.Integer(), primary_key=True),
                                    sql.Column('LOCATION_NAME', sql.String(50), nullable=False),
                                    )
        
        self.metadata.create_all(self.engine)

    def get_locations(self) -> list[dict[int, str]]:
        with LocationDatabase(self.database_path, self.table_name) as database:
            results = database.exec_query(self.location_table.select())

        return [row._asdict() for row in results]
    
    def set_locations(self, locations: list[dict]) -> None:
        rows = []

        with LocationDatabase(self.database_path, self.table_name) as database:
            for location in locations:
                row = {'LOCATION_ID': location.keys()[0], 'LOCATION_NAME': location.values()[0]}
                rows.append(row)

            df = pd.DataFrame(rows)
            df.to_sql(self.table_name, database.connection, if_exists='replace')
