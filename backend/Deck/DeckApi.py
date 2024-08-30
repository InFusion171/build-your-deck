import asyncio
import pytz
from .Deck import Deck
from ApiRequest import ApiRequest
from .DeckDatabase import DeckDatabase

from Database import Database

import urllib.parse
from datetime import datetime

class DeckApi:

    def __init__(self, top_players: dict, battlelog_url: str, api_header: str) -> None:
        self.top_players = top_players
        
        self.battlelog_url = battlelog_url
        self.api_header = api_header


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
        except:
            team_tower_troop = 159000000

       
        try:
            opponent_tower_troop = game['opponent'][0]['supportCards'][0]['id']
        except:
            opponent_tower_troop = 159000000

        team_deck = Deck(team_evo_cards, team_cards, team_tower_troop, play_date)
        opponent_deck = Deck(opponent_evo_cards, opponent_cards, opponent_tower_troop, play_date)

        if player_crowns > enemy_crowns:
            team_deck.won_count = 1
            opponent_deck.lost_count = 1

        else:
            opponent_deck.won_count = 1
            team_deck.lost_count = 1


        try:
            team_deck.trophies = game['team'][0]['startingTrophies']
            opponent_deck.trophies = game['opponent'][0]['startingTrophies']
        except:
            return None, None

        return team_deck, opponent_deck
        

    def get_decks_from_player_battelog(self, player_tag: str):
        loop = asyncio.get_event_loop()
        battlelog = loop.run_until_complete(ApiRequest.request(
                                self.battlelog_url.replace('PLAYERTAG', urllib.parse.quote(player_tag)), 
                                self.api_header))

        if not battlelog:
            print('cant get the battle log')
            return None

        decks: list[Deck] = []

        for game in battlelog:
            if not ('pathOfLegend' in game['type']):
                continue

            team_deck, opponent_deck = self._get_game_decks(game)

            if team_deck is None or opponent_deck is None:
                continue

            decks.append(team_deck)
            decks.append(opponent_deck)

        return decks
    
    def write_decks_to_db(self):
        all_decks: list[Deck] = []

        for player_tag in self.top_players.keys():
            decks_player = self.get_decks_from_player_battelog(player_tag)

            if decks_player is None:
                continue

            all_decks.extend(decks_player)

        europe_timezone = pytz.timezone('Europe/Berlin')
        current_time = datetime.now(europe_timezone)
        print("All battlelogs recivied at: ", current_time.strftime('%Y-%m-%d %H:%M'))

        with DeckDatabase() as database:
            database.add_decks(database, all_decks)

    def get_decks(self, cards: list[dict]):
        with DeckDatabase() as database:
            return database.find_highest_level_war_decks(database, cards)
            #return database.find_highest_level_deck(database, cards)