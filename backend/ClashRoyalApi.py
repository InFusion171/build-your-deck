import os
from sortedcontainers import SortedDict


class ClashRoyaleApi:
    def __init__(self, location_db_path) -> None:
        self.clash_royal_api_url = 'https://api.clashroyale.com/v1'
        self.header_for_api =  {'content-type': 'application/json', 'Authorization': 'Bearer {}'.format(os.getenv('API_TOKEN'))}
        self.ranking_list_path_of_legends_location_endpoint = '/locations/LOCATION_ID/pathoflegend/players'
        self.player_battlelog_endpoint = '/players/PLAYERTAG/battlelog'
        self.locations_list_endpoint = '/locations'

        self.location_table_name = 'countries'
        self.location_db_path = location_db_path

        self.location_list = dict()
        self.sorted_top_player = SortedDict()
        self.all_top_player_decks = dict()

    



    

