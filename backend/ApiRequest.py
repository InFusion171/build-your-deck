import aiohttp
import asyncio


class ApiRequest:
    _semaphore = asyncio.Semaphore(80)  # Limitiert auf 80 gleichzeitige Anfragen

    @staticmethod
    async def request(url: str, headers: dict):
        async with ApiRequest._semaphore:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    await asyncio.sleep(1/80)  # Pause, um das Rate-Limit zu gewährleisten

                    if response.status != 200:
                        print('Something went wrong.')
                        print(f'URL: {url}')
                        print(f'Response: {await response.text()}')
                        return None

                    return await response.json()