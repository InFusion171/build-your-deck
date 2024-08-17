from ApiRequest import ApiRequest

class PlayerApi:
    def __init__(self, top_players_url: str, api_header: str, location_list: dict) -> None:
        self.top_players_url = top_players_url
        self.api_header = api_header

        self.location_list = location_list
    
    def get_top_players(self, player_limit: int) -> dict:
        top_player = dict()

        for locationId in self.location_list.keys():
            top_players_response = ApiRequest.request(self.top_players_url.replace('LOCATION_ID', str(locationId)) + 
                                                        f'?limit={player_limit}',
                                                        self.api_header)

            if(top_players_response == None):
                continue

            for player in top_players_response['items']:
                top_player[player['tag']] = player['eloRating']

        return top_player
    