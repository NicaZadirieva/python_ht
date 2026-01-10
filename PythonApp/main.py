"""Заказ в интернет-магазине"""
from typing import Protocol
class Item:
    """Продукт"""
    def __init__(self, name: str, price: float, qty: int):
        self.name = name
        self.price = price
        self.qty = qty

    def subtotal(self):
        """Цена товара в заказе"""
        return self.price * self.qty

class DiscountPolicy(Protocol):
    """Протокол скидок"""
    def discount(self, total: float) -> float: ...


class NoDiscountPolicy(DiscountPolicy):
    """Политика: без скидки"""
    def discount(self, total: float) -> float:
        return 0

class PercentageDiscountPolicy(DiscountPolicy):
    """Политика: со  скидкой"""
    def __init__(self, percentage: int):
        self.__percentage = percentage

    def discount(self, total: float) -> float:
        return total * (1 - self.__percentage / 100)


class Order:
    def __init__(self, items: list[Item], policy: DiscountPolicy):
        self.items = items
        self.policy = policy

    def total(self):
        total_price = 0
        for item in self.items:
            total_price += item.subtotal()
        return total_price

    def total_with_discount(self):
        return self.policy.dicount(self.total())

    def set_policy(self, policy: DiscountPolicy):
        self.policy = policy