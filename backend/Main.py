from dotenv import load_dotenv
from datetime import datetime
import pytz
from ClashRoyalApi import ClashRoyaleApi

from Card.CardDatabase import CardDatabase
from Deck.DeckDatabase import DeckDatabase
from Location.LocationDatabase import LocationDatabase

def main():
    load_dotenv()

    europe_timezone = pytz.timezone('Europe/Berlin')
    current_time = datetime.now(europe_timezone)

    print("Started at:", current_time.strftime('%Y-%m-%d %H:%M'))

    CardDatabase.setup_database_connection('DB/Card.sqlite', 'cards')
    DeckDatabase.setup_database_connection('DB/Deck.sqlite', 'decks')
    LocationDatabase.setup_database_connection('DB/Location.sqlite', 'locations')

    clashApi = ClashRoyaleApi()

    clashApi.run_api()



if __name__ == '__main__':
    main()