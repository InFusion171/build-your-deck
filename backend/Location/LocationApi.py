from ApiRequest import ApiRequest
from .LocationDatabase import LocationDatabase


class LocationApi:
    def __init__(self, location_list_url: str, api_header: str, location_db_path: str, location_table_name: str):
        self.location_list_url = location_list_url
        self.api_header = api_header
        self.location_db_path = location_db_path
        self.location_table_name = location_table_name

        self.locations = dict()

    def create_and_get_locations(self) -> dict[str, str]:
        if len(self.locations) != 0:
            return self.locations
        
        with LocationDatabase(self.location_db_path, self.location_table_name) as database:
            self.locations = database.get_locations()

            if len(self.locations) != 0:
                return self.locations
            
            self.locations = self._get_location_list_from_api()

            database.set_locations(self.locations)

            return self.locations


    def _get_location_list_from_api(self) -> dict[str, str]:
        locationListResponse = ApiRequest.request(self.location_list_url, self.api_header)

        locations = dict()

        for item in locationListResponse['items']:
            if(item['isCountry'] == False):
                continue

            locations[item['id']] = item['name']

        return locations