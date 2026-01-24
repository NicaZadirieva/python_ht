import asyncio
import aiohttp

async def job():
    print("Работаю")
    await asyncio.sleep(5)
    print("Готово!")


async def main():
    task = asyncio.create_task(job())
    await asyncio.sleep(1)
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print(task.cancelled())
        print("Задача отменена")



asyncio.run(main())