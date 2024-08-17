from ApiRequest import ApiRequest
from Deck import Deck
import urllib.parse

from DeckDatabase import DeckDatabase

class PlayerApi:
    def __init__(self, battlelog_url: str, top_players_url: str, api_header: str, location_list: dict, deck_db_path:str, deck_table_name: str) -> None:
        self.battlelog_url = battlelog_url
        self.top_players_url = top_players_url
        self.api_header = api_header

        self.location_list = location_list
        self.deck_db_path = deck_db_path
        self.deck_table_name = deck_table_name


        self.top_player = dict()
        self.top_player_decks = dict()

    def __get_winning_deck(self, game):
        player_crowns = game['team'][0]['crowns']
        enemy_crowns = game['opponent'][0]['crowns']

        cards = []

        for card in game['team' if player_crowns > enemy_crowns else 'opponent'][0]['cards']:
            if 'maxEvolutionLevel' in card:
                cards.insert(0, int(card['id']))
            else:
                cards.append(int(card['id']))

        if len(cards) != 8:
            print('We need to have 8 cards')
            return None


        # get play year date and month
        play_time = game['battleTime'].strip('T')[0]

        return Deck(*cards, play_time)

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
            player_winning_decks[deck.get_id()] = deck

        return player_winning_decks
    
    def create_and_get_top_players(self, player_limit: int) -> dict:
        if len(self.top_player) != 0:
            return self.top_player

        for locationId in self.location_list.keys():
            top_players_response = ApiRequest.request(self.top_players_url.replace('LOCATION_ID', str(locationId)) + 
                                                        f'?limit={player_limit}',
                                                        self.api_header)

            if(top_players_response == None):
                continue

            for player in top_players_response['items']:
                self.top_player[player['tag']] = player['eloRating']

        return self.top_player
    
    def write_decks_to_db(self, player_count_per_region: int):
  

        #test
        """deck1 = Deck('11', '2', '3', '4', '5', '6', '7', '8', '20240811')
        deck2 = Deck('111', '22', '33', '44', '55', '66', '77', '88', '20240811')

        a = dict()
        a[deck1.__hash__()] = deck1
        a[deck2.__hash__()] = deck2

        self.top_player_decks = a"""


        with DeckDatabase(self.deck_db_path, self.deck_table_name) as database:
            for player_tag in self.create_and_get_top_players(player_count_per_region).keys():
                database.add_decks(self.get_winning_decks(player_tag))

    