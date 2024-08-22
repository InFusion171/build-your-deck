from ApiRequest import ApiRequest

class CardApi:
    def __init__(self, cards_url: str, api_header: str) -> None:
        self.cards_url = cards_url
        self.api_header = api_header

        self.cards = dict()

    def create_and_get_cards(self):
        if len(self.cards) != 0:
            return self.cards

        with LocationDatabase(self.location_db_path, self.location_table_name) as database:
            self.locations = database.get_locations()

            if len(self.locations) != 0:
                return self.locations
            
            self.locations = self._get_location_list_from_api()

            database.set_locations(self.locations)

            return self.locations

        self.cards = ApiRequest.request(self.cards_url, self.api_header)

        if cards is None:
            return None
        
