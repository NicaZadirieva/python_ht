from typing import Generic, TypeVar

Number = TypeVar("Number", int, float)

class MyMath(Generic[Number]):
    def max(self, a: Number, b: Number):
        return a if a > b else b

    def add(self, a: Number, b: Number):
        return a + b