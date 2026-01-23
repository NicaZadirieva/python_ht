import asyncio
import aiohttp

# получение в задачах конкуретно 10 раз обращение к гугл
async def main():
    async with aiohttp.ClientSession() as session:
        urls = ["https://google.com"] * 10
        tasks = [
            asyncio.create_task(session.get(url, timeout=10)) for url in urls
        ]
        done, _ = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        results = [task.result() for task in done]
        print(list(map(lambda x: x.status, results)))

asyncio.run(main())