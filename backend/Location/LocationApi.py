import asyncio
from ApiRequest import ApiRequest
from .LocationDatabase import LocationDatabase


class LocationApi:
    def __init__(self, location_list_url: str, api_header: str):
        self.location_list_url = location_list_url
        self.api_header = api_header

        self.locations = dict()

    def create_and_get_locations(self) -> dict[str, str]:
        if len(self.locations) != 0:
            return self.locations
        
        with LocationDatabase() as database:
            self.locations = database.get_locations()

            if len(self.locations) != 0:
                return self.locations
            
            self.locations = self._get_location_list_from_api()

            database.set_locations(self.locations)

            return self.locations


    def _get_location_list_from_api(self) -> dict[str, str]:
        loop = asyncio.get_event_loop()
        location_list_response = loop.run_until_complete(ApiRequest.request(self.location_list_url, self.api_header))

        if not location_list_response:
            return None

        locations = dict()

        for item in location_list_response['items']:
            if(item['isCountry'] == False):
                continue

            locations[item['id']] = item['name']

        return locations