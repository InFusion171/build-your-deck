from Database import Database
import pandas as pd

class LocationDatabase(Database):
    def __init__(self, database_path: str, table_name: str):
        super().__init__(database_path, table_name)

    def get_locations(self) -> dict:
        with LocationDatabase(self.database_path, self.table_name) as (database, _):
            results = database.exec_query(f'SELECT * FROM {self.table_name}')

        return {row[0] : row[1] for row in results}
    
    def set_locations(self, locations: dict) -> None:
        with LocationDatabase(self.database_path, self.table_name) as (database, _):
            df = pd.DataFrame([locations])
            df.to_sql(self.table_name, database.connection, if_exists='replace')
