
from numpy import sort
from sortedcontainers import SortedDict
from ApiRequest import ApiRequest
import urllib.parse

class PlayerApi:
    def __init__(self, battlelog_url: str, top_players_url: str, api_header: str, location_list: dict) -> None:
        self.battlelog_url = battlelog_url
        self.top_players_url = top_players_url
        self.api_header = api_header

        self.location_list = location_list

    def get_winning_deck(self, game):
        player_crowns = game['team'][0]['crowns']
        enemy_crowns = game['opponent'][0]['crowns']

        deck = []

        for card in game['team' if player_crowns > enemy_crowns else 'opponent'][0]['cards']:
            if 'maxEvolutionLevel' in card:
                deck.insert(0, card['id'])
            else:
                deck.append(card['id'])

        return tuple(sort(deck))

    def get_player_winning_decks(self, player_tag: str):
        battlelog = ApiRequest.request(self.battlelog_url.replace('PLAYERTAG', urllib.parse.quote(player_tag)), 
                                       self.api_header)

        if battlelog is None:
            print('cant get the battle log')
            return
        
        player_winning_decks = dict()

        for games in battlelog:
            if games['type'] is not 'pathOfLegend':
                continue

            deck = self.get_winning_deck(games)
            player_winning_decks[deck] = deck

        return player_winning_decks
    
    def get_top_players_list(self, player_limit: int) -> SortedDict:
        sorted_top_player = SortedDict()

        for _, locationId in self.location_list.items():
            top_players_response = ApiRequest.request(self.top_players_url.replace('LOCATION_ID', str(locationId)) + 
                                                        f'?limit={player_limit}',
                                                        self.api_header)

            if(top_players_response == None):
                continue

            for player in top_players_response['items']:
                sorted_top_player[player['eloRating']] = player['tag']

        return sorted_top_player