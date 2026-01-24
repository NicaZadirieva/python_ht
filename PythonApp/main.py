import asyncio
import aiohttp

async def save():
    print("Сохраняю")
    await asyncio.sleep(5)
    print("Сохранено")

async def job():
    print("Работаю")
    t = asyncio.create_task(save())
    await asyncio.shield(t)
    await asyncio.sleep(5)
    print("Готово")

async def main():
    task = asyncio.create_task(job())
    await asyncio.sleep(5)
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print(task.cancelled())
        print("Задача отменена")



asyncio.run(main())