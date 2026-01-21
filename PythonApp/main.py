from typing import TypeVar, Callable

T = TypeVar("T")
R = TypeVar("R")

def process_items(items: list[T], transformer: Callable[[T], R]):
    return [transformer(item) for item in items]

def to_upper(s: str) -> str:
    return s.upper()

result = process_items(["Anton", "Vasya"], to_upper)
    