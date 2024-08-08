import os
from sortedcontainers import SortedDict

import ApiRequest

class ClashRoyaleApi:
    def __init__(self) -> None:
        self.clashRoyalApiUrl = 'https://api.clashroyale.com/v1'
        self.headerForApi =  {'content-type': 'application/json', 'Authorization': 'Bearer {}'.format(os.getenv('API_TOKEN'))}
        self.rankingListPathOfLegendsForLocationEndpoint = '/locations/LOCATION_ID/pathoflegend/players'
        self.locationsListEndpoint = '/locations'

    def createLocationList(self) -> dict:
        locationListResponse = ApiRequest.request(self.clashRoyalApiUrl + self.locationsListEndpoint, self.headerForApi)

        self.locationMap = dict()

        for item in locationListResponse['items']:
            if(item['isCountry'] == False):
                continue

            self.locationMap[item['name']] = item['id']

        return self.locationMap

    def createTopPlayersList(self) -> SortedDict:
        self.sortedTopPlayerMap = SortedDict()

        for _, locationId in self.locationMap.items():
            topPlayersResponse = ApiRequest.request(self.clashRoyalApiUrl + 
                                                   self.rankingListPathOfLegendsForLocationEndpoint.replace('LOCATION_ID', str(locationId)) + '?limit=50',
                                                   self.headerForApi)

            if(topPlayersResponse == None):
                continue

            for player in topPlayersResponse['items']:
                self.sortedTopPlayerMap[player['eloRating']] = player['tag']

        return self.sortedTopPlayerMap