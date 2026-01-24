import asyncio
import random

async def unstable():
    await asyncio.sleep(0.2)
    if random.random() < 0.5:
        raise ValueError("Случайная ошибка")
    return "OK"

async def run_with_retry(job, max_retries=3):
    for attempt in range(1, max_retries + 1):
        task = asyncio.create_task(job())
        try:
            result = await task
            print(f"Попытка {attempt}: успех -> {result}")
            return result
        except Exception as e:
            print(f"Попытка {attempt}: ошибка -> {e}")

            if attempt == max_retries:
                print("Все попытки исчерпаны")
                return "ERROR"
            await asyncio.sleep(0.5)
    

async def main():
    # run_with_retry - сделать корутину, которая запустит корутину
    # если она выбросила ошибку, пробует заново до указанного лимита
    result = await run_with_retry(unstable)
    print(f"Итог: {result}")


asyncio.run(main())