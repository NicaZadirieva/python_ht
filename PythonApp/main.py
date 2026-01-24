import asyncio
import random

async def unstable():
    await asyncio.sleep(0.2)
    if random.random() < 0.5:
        raise ValueError("Случайная ошибка")
    return "OK"

async def run_with_retry(task, max_count=5):
    for _ in range(max_count - 1):
        try:
            res = await task
            return res
        except:
            pass
    res = await task
    return res
    

async def main():
    # run_with_retry - сделать корутину, которая запустит корутину
    # если она выбросила ошибку, пробует заново до указанного лимита
    res = await run_with_retry(asyncio.create_task(unstable()))
    print(res)


asyncio.run(main())