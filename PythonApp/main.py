import asyncio
import random

async def unstable():
    await asyncio.sleep(0.2)
    if random.random() < 0.5:
        raise ValueError("Случайная ошибка")
    return "OK"

async def main():
    # run_with_retry - сделать корутину, которая запустит корутину
    # если она выбросила ошибку, пробует заново до указанного лимита
    pass


asyncio.run(main())