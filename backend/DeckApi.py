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


    def _get_game_decks(self, game):
        player_crowns = game['team'][0]['crowns']
        enemy_crowns = game['opponent'][0]['crowns']

        team_cards = []
        team_evo_cards = []

        opponent_cards = []
        opponent_evo_cards = []

        for card in game['team'][0]['cards']:
            if 'evolutionLevel' in card:
                team_evo_cards.append(int(card['id']))
            else:
                team_cards.append(int(card['id']))

        for card in game['opponent'][0]['cards']:
            if 'evolutionLevel' in card:
                opponent_evo_cards.append(int(card['id']))
            else:
                opponent_cards.append(int(card['id']))

    
        play_date = game['battleTime']

        try:
            team_tower_troop = game['team'][0]['supportCards'][0]['id']
            opponent_tower_troop = game['opponent'][0]['supportCards'][0]['id']
        except:
            print(f'error! Game:\n{game}')
            return None
       
        team_deck = Deck(team_evo_cards, team_cards, team_tower_troop, play_date)
        opponent_deck = Deck(opponent_evo_cards, opponent_cards, opponent_tower_troop, play_date)

        if player_crowns > enemy_crowns:
            team_deck.won_count = 1
            opponent_deck.lost_count = 1
        else:
            opponent_deck.won_count = 1
            team_deck.lost_count = 1

        return team_deck, opponent_deck
        

    def get_decks_from_player_battelog(self, player_tag: str):
        battlelog = ApiRequest.request(self.battlelog_url.replace('PLAYERTAG', urllib.parse.quote(player_tag)), 
                                       self.api_header)

        if battlelog is None:
            print('cant get the battle log')
            return None
        
        decks: list[Deck] = []

        for game in battlelog:
            if not ('pathOfLegend' in game['type']):
                continue

            deck = self._get_game_decks(game)

            if deck is None:
                continue

            decks.extend([*deck])


        bundled_decks: dict[str, Deck] = dict()

        for deck in decks:
            id = deck.get_id()

            if id in bundled_decks:
                bundled_decks[id].won_count = bundled_decks.get(id).won_count + deck.won_count
                bundled_decks[id].lost_count = bundled_decks.get(id).lost_count + deck.lost_count
            else:
                bundled_decks[id] = deck

        return bundled_decks
    
    def write_decks_to_db(self):
        with DeckDatabase(self.deck_db_path, self.deck_table_name) as database:
            for player_tag in self.top_players.keys():
                database.add_decks(database, self.get_decks_from_player_battelog(player_tag))