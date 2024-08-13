import os
from sortedcontainers import SortedDict

from ApiRequest import ApiRequest
from LocationDatabase import LocationDatabase

class ClashRoyaleApi:
    def __init__(self, location_db_path) -> None:
        self.clash_royal_api_url = 'https://api.clashroyale.com/v1'
        self.header_for_api =  {'content-type': 'application/json', 'Authorization': 'Bearer {}'.format(os.getenv('API_TOKEN'))}
        self.ranking_list_path_of_legends_location_endpoint = '/locations/LOCATION_ID/pathoflegend/players'
        self.locations_list_endpoint = '/locations'

        self.location_table_name = 'countries'
        self.location_db_path = location_db_path

        self.location_list = dict()
        self.sorted_top_player = SortedDict()

    def get_location_list(self) -> dict:
        if(len(self.location_list) != 0):
            return self.location_list
        
        with LocationDatabase(self.location_db_path, self.location_table_name) as (database, exists):
            if exists:
                self.location_list = database.get_locations()
                return self.location_list
            
            self.location_list = self.get_location_list_from_api()

            database.set_locations(self.location_list)
            
            return self.location_list


    def get_location_list_from_api(self) -> dict:
        locationListResponse = ApiRequest.request(self.clash_royal_api_url + self.locations_list_endpoint, self.header_for_api)

        location_list = dict()

        for item in locationListResponse['items']:
            if(item['isCountry'] == False):
                continue

            location_list[item['name']] = item['id']

        return location_list

    def create_top_players_list(self, player_limit: int) -> SortedDict:
        sorted_top_player = SortedDict()

        for _, locationId in self.location_list.items():
            top_players_response = ApiRequest.request(self.clash_royal_api_url + 
                                                   self.ranking_list_path_of_legends_location_endpoint.replace('LOCATION_ID', str(locationId)) + f'?limit={player_limit}',
                                                   self.header_for_api)

            if(top_players_response == None):
                continue

            for player in top_players_response['items']:
                sorted_top_player[player['eloRating']] = player['tag']

        self.sorted_top_player = sorted_top_player

        return sorted_top_player