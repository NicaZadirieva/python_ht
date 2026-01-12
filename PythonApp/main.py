"""Dependency Inversion Principle"""

"""
Модули верхних уровней не должны напрямую зависеть от модулей нижних уровней.
Оба типа модулей должны зависеть от абстракций, а не абстракции от деталей.
"""

"""
Сделать LowStockService который в методе run проверяет в 
InMemoryStockRepository - сколько осталось товара (число items)
и если их меньше 10 - отправляет уведомление через EmailNotifier
"""

from dataclasses import dataclass, field
from typing import Protocol


class StockRepository(Protocol):
    def get_stock_count(self):
        pass


class Notifier(Protocol):
    def notify(self, msg: str):
        pass

@dataclass
class InMemoryStockRepository(StockRepository):
    items: list[str] = field(default_factory=list)

    def add_item(self, item: str):
        self.items.append(item)
        return item

    def remove_item(self, item: str):
        self.items.remove(item)
        return item

    def get_stock_count(self):
        return len(self.items)

@dataclass
class EmailNotifier(Notifier):
    def notify(self, msg: str):
        print(f"Отправка email: {msg}")


@dataclass
class LowStockService:
    notifier: Notifier
    stockRepo: StockRepository

    def run(self) -> None:
        if self.stockRepo.get_stock_count() < 10:
            self.notifier.notify("[LowStockRepo]: остаток менее 10 единиц")
        else:
            self.notifier.notify("[LowStockRepo]: проверка пройдена")


stockRepo = InMemoryStockRepository(["apple", "tomato", "potato"])
notifier = EmailNotifier()
lowStockService = LowStockService(notifier, stockRepo)

lowStockService.run()