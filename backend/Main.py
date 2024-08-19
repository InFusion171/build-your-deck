from dotenv import load_dotenv
from datetime import datetime
import pytz
from ClashRoyalApi import ClashRoyaleApi

            
def main():
    load_dotenv()

    europe_timezone = pytz.timezone('Europe/Berlin')

    current_time = datetime.now(europe_timezone)

    print("Started at:", current_time.strftime('%Y-%m-%d %H:%M'))

    clashApi = ClashRoyaleApi('DB/Location.sqlite', 'DB/Deck.sqlite')

    clashApi.run_api()


if __name__ == '__main__':
    main()