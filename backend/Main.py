from dotenv import load_dotenv

from ClashRoyalApi import ClashRoyaleApi

            
def main():
    load_dotenv()

    clashApi = ClashRoyaleApi('DB/countries.db')

    print(clashApi.create_location_list())


if __name__ == '__main__':
    main()