import asyncio
import aiohttp

async def bad():
    print("Начата")
    raise ValueError("Error")

# получение в задачах конкуретно 10 раз обращение к гугл
async def main():
    try:
        task = asyncio.create_task(bad())
        task.add_done_callback(lambda t: print("Ошибка", t.exception()))
        await asyncio.sleep(2)
        print("Ждем")
        await task
    except ValueError as e:
        print(e)

asyncio.run(main())