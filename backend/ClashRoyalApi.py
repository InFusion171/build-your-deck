from datetime import datetime
import pytz
import os

from Location.LocationApi import LocationApi
from PlayerApi import PlayerApi
from Deck.DeckApi import DeckApi

from Card.CardApi import CardApi

class ClashRoyaleApi:
    def __init__(self) -> None:
        self.clash_royal_api_url = 'https://api.clashroyale.com/v1'
        self.api_header =  {'content-type': 'application/json', 'Authorization': 'Bearer {}'.format(os.getenv('API_TOKEN'))}
        self.ranking_list_path_of_legends_location_endpoint = '/locations/LOCATION_ID/pathoflegend/players'
        self.player_battlelog_endpoint = '/players/PLAYERTAG/battlelog'
        self.player_information_endpoint = '/players/PLAYERTAG'
        self.locations_list_endpoint = '/locations'
        self.cards_list_endpoint = '/cards'

        self.card_icon_url = 'https://api-assets.clashroyale.com/cards/300'
        self.card_icon_evolution_url = 'https://api-assets.clashroyale.com/cardevolutions/300'

        self.top_player_decks = dict()
    
    def run_api(self):
        locationApi = LocationApi(self.clash_royal_api_url + self.locations_list_endpoint,
                                  self.api_header)

        self.location_list = locationApi.create_and_get_locations()

        cardApi = CardApi(self.clash_royal_api_url + self.cards_list_endpoint,
                          self.api_header)
        
        cardApi.create_and_get_cards()
        
        playerApi = PlayerApi(self.clash_royal_api_url + self.ranking_list_path_of_legends_location_endpoint,
                              self.clash_royal_api_url + self.player_information_endpoint,
                              self.api_header,
                              self.location_list
                              )
        
        top_players = playerApi.get_top_players(1)
        
        europe_timezone = pytz.timezone('Europe/Berlin')
        current_time = datetime.now(europe_timezone)
        print("All top player recieved at:", current_time.strftime('%Y-%m-%d %H:%M'))

        deckApi = DeckApi(top_players, 
                          self.clash_royal_api_url + self.player_battlelog_endpoint,
                          self.api_header)

        #print(deckApi.get_decks(playerApi.get_player_cards('#8LPG880JR')).__str__())

        deckApi.write_decks_to_db()
        




    

