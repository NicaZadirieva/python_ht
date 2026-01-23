import asyncio
import requests
import aiohttp

# получение в задачах конкуретно 10 раз обращение к гугл
async def main():
    async with aiohttp.ClientSession() as session:
        urls = ["https://google.com"] * 10
        tasks = [session.get(url, timeout=10) for url in urls]
        results = await asyncio.gather(*tasks)
        print(list(map(lambda x: x.status, results)))

asyncio.run(main())