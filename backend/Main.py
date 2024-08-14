from dotenv import load_dotenv

from ClashRoyalApi import ClashRoyaleApi

            
def main():
    load_dotenv()

    clashApi = ClashRoyaleApi('DB/Location.db')

    clashApi.setup()


if __name__ == '__main__':
    main()