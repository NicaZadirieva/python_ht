from typing import Generic, TypeVar

T = TypeVar("T", int, float)

class MyMath(Generic[T]):
    def max(self, a: T, b: T):
        return a if a > b else b

    def add(self, a: T, b: T):
        return a + b