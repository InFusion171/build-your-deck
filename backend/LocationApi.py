from ApiRequest import ApiRequest
from LocationDatabase import LocationDatabase


class LocationApi:
    def __init__(self, location_list_url: str, api_header: str, location_db_path: str, location_table_name: str):
        self.location_list_url = location_list_url
        self.api_header = api_header
        self.location_db_path = location_db_path
        self.location_table_name = location_table_name

        self.location_list = dict()

    def create_and_get_locations(self) -> dict:
        if(len(self.location_list) != 0):
            return self.location_list
        
        with LocationDatabase(self.location_db_path, self.location_table_name) as (database, exists):
            if exists:
                self.location_list = database.get_locations()
                return self.location_list
            
            self.location_list = self.__get_location_list_from_api()

            database.set_locations(self.location_list)
            
            return self.location_list


    def __get_location_list_from_api(self) -> dict:
        locationListResponse = ApiRequest.request(self.location_list_url, self.api_header)

        location_list = dict()

        for item in locationListResponse['items']:
            if(item['isCountry'] == False):
                continue

            location_list[item['name']] = item['id']

        return location_list