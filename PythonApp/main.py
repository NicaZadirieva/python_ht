"""
Нужно сделать Repository, который работает с любыми типами и имеет методы:
- add - добавляет в список элемент
- get_by_index - получает по index
- get_all - получает все

Все хранится в list
"""

from dataclasses import dataclass
from typing import Optional, TypeVar, Generic

T = TypeVar("T")

@dataclass
class Repository(Generic[T]):
    items: list[T]

    def add(self, item: T) -> T:
        self.items.append(item)
        return item

    def get_by_index(self, index: int) -> Optional[T]:
        return None if index >= len(self.items) else self.items[index] 

    def get_all(self) -> list[T]:
        return self.items

repo = Repository[int]([1, 2, 3])
print(repo.add(4))

print(repo.get_by_index(2))
print(repo.get_all())