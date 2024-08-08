import requests
import time

class ApiRequest:
    def request(url: str, header: str):
        response = requests.get(url, headers=header)

        time.sleep(1)

        if(response.status_code != 200):
            print('Something went wrong.')
            print(f'URL: {url}')
            print(f'response: {response.text}')

            return None


        return response.json()