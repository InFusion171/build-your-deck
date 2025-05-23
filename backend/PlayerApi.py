import asyncio
from ApiRequest import ApiRequest
from Card.Card import Card
import urllib.parse
import os

from BoostedCard.BoostedCardDatabase import BoostedCardDatabase 

class PlayerApi:
    def __init__(self, top_players_url: str, player_information_url: str, api_header: str, location_list: dict) -> None:
        self.top_players_url = top_players_url
        self.player_information_url = player_information_url
        self.api_header = api_header

        self.location_list = location_list
    
    def _player_level_to_crown_level(self, player_level: int):
        levels = [
            (54, 15), (42, 14), (38, 13), (34, 12), 
            (30, 11), (26, 10), (22, 9), (18, 8), 
            (14, 7), (10, 6), (7, 5), (5, 4), 
            (3, 3), (2, 2)
        ]
        
        for level, crown in levels:
            if player_level >= level:
                return crown
            
        return 1


    def get_player_cards(self, player_tag: str) -> list[dict]:
        loop = asyncio.get_event_loop()
        player_infos = loop.run_until_complete(ApiRequest.request(
                                self.player_information_url.replace('PLAYERTAG', 
                                urllib.parse.quote(player_tag)), 
                                self.api_header))

        if player_infos is None:
            print('cant get player infos')
            return None
        
        player_level = player_infos['expLevel']

        player_crown_level = self._player_level_to_crown_level(player_level)

        boosted_cards = BoostedCardDatabase().get_boosted_cards()

        cards = []

        for card_item in player_infos['cards']:
            card = dict()
            card['name'] = card_item['name']
            card['id'] = card_item['id']
            card['rarity'] = card_item['rarity']

            if card_item['id'] in boosted_cards:
                card['level'] = max(player_crown_level, Card.normalize_card_level(card['rarity'], card_item['level']))
            else:
                card['level'] = Card.normalize_card_level(card['rarity'], card_item['level'])

            if 'evolutionLevel' in card_item:
                card['evolutionLevel'] = int(card_item['evolutionLevel'])

            cards.append(card)

        return cards

    def get_top_players(self, player_limit: int) -> dict:
        top_player = dict()

        test_count_request = 0

        for locationId in self.location_list.keys():
            if os.getenv('BUILD_YOUR_DECK_TEST') == 'TRUE':
                if test_count_request == 5:
                    break
                test_count_request += 1

            loop = asyncio.get_event_loop()
            top_players_response = loop.run_until_complete(
                                    ApiRequest.request(self.top_players_url.replace('LOCATION_ID', str(locationId)) + 
                                    f'?limit={player_limit}',
                                    self.api_header))


            if(top_players_response == None):
                continue

            for player in top_players_response['items']:
                top_player[player['tag']] = player['eloRating']

        return top_player
    