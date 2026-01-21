from typing import TypeVar

T = TypeVar("T")

def first_item(items: list[T]) -> T:
    return items[0]


users = ["Anton", "Vasya"]
num = [1, 2, 3]

res = first_item(users)
    