import json
import os
from sortedcontainers import SortedDict

from LocationApi import LocationApi
from PlayerApi import PlayerApi
from DeckDatabase import DeckDatabase
from DeckApi import DeckApi

class ClashRoyaleApi:
    def __init__(self, location_db_path: str, deck_db_path: str) -> None:
        self.clash_royal_api_url = 'https://api.clashroyale.com/v1'
        self.api_header =  {'content-type': 'application/json', 'Authorization': 'Bearer {}'.format(os.getenv('API_TOKEN'))}
        self.ranking_list_path_of_legends_location_endpoint = '/locations/LOCATION_ID/pathoflegend/players'
        self.player_battlelog_endpoint = '/players/PLAYERTAG/battlelog'
        self.locations_list_endpoint = '/locations'

        self.location_table_name = 'locations'
        self.location_db_path = location_db_path

        self.deck_table_name = 'decks'
        self.deck_db_path = deck_db_path

        self.top_player_decks = dict()
    
    def run_api(self):
        locationApi = LocationApi(self.clash_royal_api_url + self.locations_list_endpoint,
                                  self.api_header,
                                  self.location_db_path,
                                  self.location_table_name)

        self.location_list = locationApi.create_and_get_locations()


        playerApi = PlayerApi(self.clash_royal_api_url + self.ranking_list_path_of_legends_location_endpoint,
                              self.api_header,
                              self.location_list
                              )
        
        top_players = playerApi.get_top_players(100)

        deckApi = DeckApi(top_players, 
                          self.clash_royal_api_url + self.player_battlelog_endpoint,
                          self.api_header,
                          self.deck_db_path,
                          self.deck_table_name)

        #deckApi.write_decks_to_db()




    

