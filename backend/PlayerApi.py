
from numpy import sort
from sortedcontainers import SortedDict
from ApiRequest import ApiRequest
from Deck import Deck
import urllib.parse

class PlayerApi:
    def __init__(self, battlelog_url: str, top_players_url: str, api_header: str, location_list: dict) -> None:
        self.battlelog_url = battlelog_url
        self.top_players_url = top_players_url
        self.api_header = api_header

        self.location_list = location_list

        self.sorted_player_decks = SortedDict()
        self.top_player_decks = dict()

    def __get_winning_deck(self, game):
        player_crowns = game['team'][0]['crowns']
        enemy_crowns = game['opponent'][0]['crowns']

        cards = []

        for card in game['team' if player_crowns > enemy_crowns else 'opponent'][0]['cards']:
            if 'maxEvolutionLevel' in card:
                cards.insert(0, card['id'])
            else:
                cards.append(card['id'])

        if len(cards) != 8:
            print('We need to have 8 cards')
            return None

        return Deck(*cards)

    def get_winning_decks(self, player_tag: str):
        battlelog = ApiRequest.request(self.battlelog_url.replace('PLAYERTAG', urllib.parse.quote(player_tag)), 
                                       self.api_header)

        if battlelog is None:
            print('cant get the battle log')
            return dict()
        
        player_winning_decks = dict()

        for games in battlelog:
            if not ('pathOfLegend' in games['type']):
                continue

            deck = self.__get_winning_deck(games)
            player_winning_decks[deck] = deck

        return player_winning_decks
    
    def create_and_get_top_players(self, player_limit: int) -> SortedDict:
        if len(self.sorted_player_decks) != 0:
            return self.sorted_player_decks

        sorted_top_player = SortedDict()

        for locationId in self.location_list.values():
            top_players_response = ApiRequest.request(self.top_players_url.replace('LOCATION_ID', str(locationId)) + 
                                                        f'?limit={player_limit}',
                                                        self.api_header)

            if(top_players_response == None):
                continue

            for player in top_players_response['items']:
                sorted_top_player[player['eloRating']] = player['tag']

        self.sorted_top_player = sorted_top_player

        return sorted_top_player
    
    def create_and_get_top_player_decks(self, player_count_per_region: int):
        if len(self.top_player_decks) != 0:
            return self.top_player_decks
    
        deck1 = Deck('1', '2', '3', '4', '5', '6', '7', '8')
        deck2 = Deck('11', '22', '33', '44', '55', '66', '77', '88')

        a = dict()
        a[deck1] = deck1
        a[deck2] = deck2

        self.top_player_decks = a

        #for player_tag in self.create_and_get_top_players(player_count_per_region).values():
            #self.top_player_decks = self.top_player_decks | self.get_winning_decks(player_tag)

        return self.top_player_decks