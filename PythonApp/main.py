"""Заказ в интернет-магазине"""

class Item:
    """Продукт"""
    def __init__(self, name: str, price: float, qty: int):
        self.name = name
        self.price = price
        self.qty = qty

    def subtotal(self):
        """Цена товара в заказе"""
        return self.price * self.qty

class Policy:
    pass

class NoDiscountPolicy(Policy):
    """Политика: без скидки"""
    pass

class PercentageDiscountPolicy(Policy):
    """Политика: со  скидкой"""
    def __init__(self, percentage: int):
        self.__percentage = percentage

    def get_percentage(self):
        return self.__percentage


class Order:
    def __init__(self, items: list[Item], policy: Policy):
        self.items = items
        self.policy = policy

    def total(self):
        total_price = 0
        for item in self.items:
            total_price += item.subtotal()
        return total_price

    def total_with_discount(self):
        if isinstance(self.policy, NoDiscountPolicy):
            return self.total()
        elif isinstance(self.policy, PercentageDiscountPolicy):
            return self.total() * (1 - self.policy.get_percentage() / 100)
        else:
            raise ValueError("Не правильно задана политика цен")

    def set_policy(self, policy: Policy):
        self.policy = policy