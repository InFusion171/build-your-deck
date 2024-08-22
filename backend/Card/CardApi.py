from ApiRequest import ApiRequest

from CardDatabase import CardDatabase

class CardApi:
    def __init__(self, card_db_path: str, card_table_name: str, cards_url: str, api_header: str) -> None:
        self.cards_url = cards_url
        self.api_header = api_header
        self.card_db_path = card_db_path
        self.card_table_name = card_table_name

        self.cards = dict()

    def create_and_get_cards(self, overwrite_db_entries = False):
        if len(self.cards) != 0 and not overwrite_db_entries:
            return self.cards

        with CardDatabase(self.card_db_path, self.card_table_name) as database:
            self.locations = database.get_locations()

            if len(self.locations) != 0:
                return self.locations
            
            self.locations = self._get_location_list_from_api()

            database.set_locations(self.locations)

            return self.locations

        self.cards = ApiRequest.request(self.cards_url, self.api_header)

        if cards is None:
            return None
        
