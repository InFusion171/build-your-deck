from dotenv import load_dotenv

from ClashRoyalApi import ClashRoyaleApi

            
def main():
    load_dotenv()

    clashApi = ClashRoyaleApi()

    clashApi.setupLocationList()
    
    #with open('locationList.json', 'w') as f:
     #   json.dump(clashApi.locationMap, f, indent=4)

    clashApi.setupTopPlayers()

    #with open('topPlayers.json', 'w') as f:
        #json.dump(clashApi.sortedTopPlayerMap, f, indent=4)

if __name__ == '__main__':
    main()