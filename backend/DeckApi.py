from Deck import Deck
from ApiRequest import ApiRequest
from DeckDatabase import DeckDatabase

import urllib.parse

class DeckApi:

    def __init__(self, top_players: dict, battlelog_url: str, api_header: str, deck_db_path: str, deck_table_name: str) -> None:
        self.top_players = top_players
        
        self.battlelog_url = battlelog_url
        self.api_header = api_header
        
        self.deck_db_path = deck_db_path
        self.deck_table_name = deck_table_name


    def _get_winning_deck(self, game):
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
        play_date = game['battleTime'].split('T')[0]

        return Deck(*cards, play_date)

    def get_winning_decks(self, player_tag: str):
        battlelog = ApiRequest.request(self.battlelog_url.replace('PLAYERTAG', urllib.parse.quote(player_tag)), 
                                       self.api_header)

        if battlelog is None:
            print('cant get the battle log')
            return dict()
        
        player_winning_decks = dict()

        for game in battlelog:
            if not ('pathOfLegend' in game['type']):
                continue

            deck = self._get_winning_deck(game)
            player_winning_decks[deck.get_id()] = deck

        return player_winning_decks
    
    def write_decks_to_db(self):
        with DeckDatabase(self.deck_db_path, self.deck_table_name) as database:
            for player_tag in self.top_players.keys():
                database.add_decks(database, self.get_winning_decks(player_tag))