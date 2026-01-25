"""
async def send_email(user: str) -> None:

Имитация отправки письма пользователю:

ждёт случайное время от 0.3 до 0.8 секунд
печатает: "Email sent to {user}"
async def send_bulk(users: list[str]) -> None:

Должна:

запустить send_email для каждого пользователя ПАРАЛЛЕЛЬНО
 дождаться завершения всех отправок
async def main() -> None:
users = ["alice", "bob", "carol", "dave", "eve"]
await send_bulk(users)
"""

import asyncio
import random


async def send_email(user: str) -> None:
    duration_task = random.uniform(0.3, 0.8)
    await asyncio.sleep(duration_task)
    print(f"Email sent to {user}")

async def send_bulk(users: list[str]) -> None:
    tasks = [asyncio.create_task(send_email(user)) for user in users]
    done, _ = await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)
    if len(done) == len(users):
        print("Sent successfully")

async def main() -> None:
    users = ["alice", "bob", "carol", "dave", "eve"]
    await send_bulk(users)

asyncio.run(main())