from ApiRequest import ApiRequest

from .CardDatabase import CardDatabase

class CardApi:
    def __init__(self, cards_url: str, api_header: str) -> None:
        self.cards_url = cards_url
        self.api_header = api_header

        self.cards = list(dict())

    def create_and_get_cards(self, overwrite_db_entries = False) -> list[dict]:
        if len(self.cards) != 0 and not overwrite_db_entries:
            return self.cards

        with CardDatabase() as database:
            self.db_column_names = database.column_names

            if overwrite_db_entries:
                self.cards = self._get_cards_from_api()
                database.set_cards(self.cards)

                return self.cards
            
            self.cards = database.get_all_cards()

            if len(self.cards) != 0:
                return self.cards

            self.cards = self._get_cards_from_api()

            database.set_cards(self.cards)

            return self.cards

        
    def _get_cards_from_api(self) -> list[dict]:
        cards_response = ApiRequest.request(self.cards_url, self.api_header)

        if cards_response is None:
            print('cant get cards from api')
            return None

        cards = []

        for card_item in cards_response['items']:
            card = dict()

            card[self.db_column_names['card_id']] = card_item['id']
            card[self.db_column_names['card_name']] = card_item['name']
            card[self.db_column_names['card_max_level']] = card_item['maxLevel']
            card[self.db_column_names['card_rarity']] = card_item['rarity']

            if 'maxEvolutionLevel' in card_item:
                card[self.db_column_names['card_max_evolution_level']] = int(card_item['maxEvolutionLevel'])

                evolution_icon_url: str = card_item['iconUrls']['evolutionMedium']

                card[self.db_column_names['card_icon_evolution']] = evolution_icon_url.split('/')[len(evolution_icon_url.split('/'))-1]

            card_icon_url: str = card_item['iconUrls']['medium']

            card[self.db_column_names['card_icon']] = card_icon_url.split('/')[len(card_icon_url.split('/'))-1]

            cards.append(card)

        return cards


