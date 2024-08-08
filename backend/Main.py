from dotenv import load_dotenv

from ClashRoyalApi import ClashRoyaleApi

            
def main():
    load_dotenv()

    clashApi = ClashRoyaleApi()

    clashApi.createLocationList()

    clashApi.createTopPlayersList()

if __name__ == '__main__':
    main()