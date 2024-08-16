from dotenv import load_dotenv

from ClashRoyalApi import ClashRoyaleApi

            
def main():
    load_dotenv()

    clashApi = ClashRoyaleApi('DB/Location.sqlite', 'DB/Deck.sqlite')

    clashApi.run_api()


if __name__ == '__main__':
    main()