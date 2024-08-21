from ApiRequest import ApiRequest

import os

class PlayerApi:
    def __init__(self, top_players_url: str, api_header: str, location_list: dict) -> None:
        self.top_players_url = top_players_url
        self.api_header = api_header

        self.location_list = location_list
    
    def get_top_players(self, player_limit: int) -> dict:
        top_player = dict()

        test_count_request = 0

        for locationId in self.location_list.keys():
            if os.getenv('BUILD_YOUR_DECK_TEST') == 'TRUE':
                if test_count_request == 10:
                    break
                test_count_request = test_count_request + 1



            top_players_response = ApiRequest.request(self.top_players_url.replace('LOCATION_ID', str(locationId)) + 
                                                        f'?limit={player_limit}',
                                                        self.api_header)

            if(top_players_response == None):
                continue

            for player in top_players_response['items']:
                top_player[player['tag']] = player['eloRating']


        #top_player['#8lpg880jr'] = 123


        return top_player
    