import os
from dotenv import load_dotenv
from sortedcontainers import SortedDict

import ApiRequest


class clashRoyaleApi:
    def __init__(self) -> None:
        self.clashRoyalApiUrl = 'https://api.clashroyale.com/v1'
        self.headerForApi =  {'content-type': 'application/json', 'Authorization': 'Bearer {}'.format(os.getenv('API_TOKEN'))}
        self.rankingListPathOfLegendsForLocationEndpoint = '/locations/LOCATION_ID/pathoflegend/players'
        self.locationsListEndpoint = '/locations'

    def setupLocationList(self):
        locationListResponse = ApiRequest.request(self.clashRoyalApiUrl + self.locationsListEndpoint, self.headerForApi)

        self.locationMap = dict()

        for item in locationListResponse['items']:
            if(item['isCountry'] == False):
                continue

            self.locationMap[item['name']] = item['id']

    def setupTopPlayers(self):
        self.sortedTopPlayerMap = SortedDict()

        for _, locationId in self.locationMap.items():
            topPlayersResponse = ApiRequest.request(self.clashRoyalApiUrl + 
                                                   self.rankingListPathOfLegendsForLocationEndpoint.replace('LOCATION_ID', str(locationId)) + '?limit=50',
                                                   self.headerForApi)

            if(topPlayersResponse == None):
                continue

            for player in topPlayersResponse['items']:
                self.sortedTopPlayerMap[player['eloRating']] = player['tag']


            
def main():
    load_dotenv()

    clashApi = clashRoyaleApi()

    clashApi.setupLocationList()
    
    #with open('locationList.json', 'w') as f:
     #   json.dump(clashApi.locationMap, f, indent=4)

    clashApi.setupTopPlayers()

    #with open('topPlayers.json', 'w') as f:
        #json.dump(clashApi.sortedTopPlayerMap, f, indent=4)

if __name__ == '__main__':
    main()