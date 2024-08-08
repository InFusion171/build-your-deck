from Database import Database
import pandas as pd

class LocationDatabase(Database):
    def __init__(self, database_path: str, table_name: str):
        super().__init__(database_path, table_name)

    def get_locations(self) -> dict:
        results = self.exec_query(f'SELECT * FROM {self.table_name}')

        return {row[0] : row[1] for row in results}
    
    def set_locations(self, locations: dict) -> None:
        self.open_db_connection()

        df = pd.DataFrame(locations)

        df.to_sql(self.table_name, self.db_conn, if_exists='replace')
