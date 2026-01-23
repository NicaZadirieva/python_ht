import asyncio
import time

def fetch():
    time.sleep(2)
    return "done"

def main():
    for _ in range(3):
        print(fetch())

main()