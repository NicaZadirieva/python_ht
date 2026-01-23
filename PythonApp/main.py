import asyncio
import requests
import aiohttp

async def main():
    #res = requests.get("https://google.com", timeout=10)
    #print(res.status_code)
    async with aiohttp.ClientSession() as session:
        res = await session.get("https://google.com", timeout=10)
        print(res.status)

asyncio.run(main())