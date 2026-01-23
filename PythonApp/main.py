import asyncio
import requests
import aiohttp

# получение в задачах конкуретно 10 раз обращение к гугл
async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [session.get("https://google.com", timeout=10) for _ in range(10)]
        results = await asyncio.gather(*tasks)
        print(",".join([str(r.status) for r in results]))

asyncio.run(main())