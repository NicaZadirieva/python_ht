from dataclasses import dataclass, field
from typing import Optional, TypeVar, Generic

K = TypeVar("K")
V = TypeVar("V")

@dataclass
class Cache(Generic[K, V]):
    __cache__: dict[K, V] = field(default_factory=dict)

    def get(self, key: K) -> Optional[V]:
        if not isinstance(key, type(K)):
            raise TypeError("Ошибка типов")
        if key in self.__cache__:
            return self.__cache__[key]
        return None

    def set(self, key: K, value: V) -> None:
        if not isinstance(key, type(K)) or not isinstance(value, type(V)):
            raise TypeError("Ошибка типов")
        self.__cache__[key] = value

    def keys(self) -> list[K]:
        return list(self.__cache__.keys())

    def values(self) -> list[V]:
        return list(self.__cache__.values())

hits = Cache[str, int]()
hits.set("home", 10)
hits.set("about", 3)
x = hits.get("home")        # x: int | None
paths = hits.keys()         # list[str]
counts = hits.values()      # list[int]

hits.set("contacts", "5")   # ❌ ошибка типов
hits.get(123)               # ❌ ошибка типов
