import asyncio
import aiohttp

async def fetch(session, url):
    return await asyncio.wait_for(session.get(url), timeout=2)

# получение в задачах конкуретно 10 раз обращение к гугл
async def main():
    async with aiohttp.ClientSession() as session:
        urls = ["https://google.com"] * 10
        tasks = [
            asyncio.create_task(fetch(session, url)) for url in urls
        ]
        done, _ = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        results = [task.result() for task in done]
        print(list(map(lambda x: x.status, results)))

asyncio.run(main())