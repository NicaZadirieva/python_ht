import asyncio

async def get_message():
    return "Привет";

async def main():
    result = await asyncio.create_task(get_message())
    print(result)

asyncio.run(main())