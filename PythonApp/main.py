import asyncio
import time

async def fetch():
    time.sleep(2) # блокирует поток
    return "done"

async def main():
    tasks = [fetch() for _ in range(3)]
    results = await asyncio.gather(*tasks)
    print(results)

asyncio.run(main())