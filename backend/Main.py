from dotenv import load_dotenv
from datetime import datetime
import pytz
from ClashRoyalApi import ClashRoyaleApi
from Card.CardDatabase import CardDatabase
            
def main():
    load_dotenv()

    europe_timezone = pytz.timezone('Europe/Berlin')

    current_time = datetime.now(europe_timezone)

    print("Started at:", current_time.strftime('%Y-%m-%d %H:%M'))

    CardDatabase.setup_database_connection('DB/Card.sqlite', 'cards')

    clashApi = ClashRoyaleApi('DB/Location.sqlite', 'DB/Deck.sqlite', 'DB/Card.sqlite')

    clashApi.run_api()

    print("All Decks wrote to db at:", current_time.strftime('%Y-%m-%d %H:%M'))


if __name__ == '__main__':
    main()