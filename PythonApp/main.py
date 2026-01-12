"""Принцип открытости-закрытости"""
"""Классы должны быть открыты для расширения, но закрыты для модификации."""

#class DiscountCalculator:
#    """Нарушение принципа, так как может измениться логика user_type"""
#    def calculate(self, user_type: str, amount: float) -> float:
#        if user_type == "student":
#            return amount * 0.9
#        elif user_type == "vip":
#            return amount * 0.8
#        else:
#            return amount

from abc import ABC, abstractmethod
from dataclasses import dataclass

class DiscountPolicy(ABC):
    @abstractmethod
    def apply_discount(self, amount: float) -> float:
        pass

class NoDiscount(DiscountPolicy):
    def apply_discount(self, amount: float) -> float:
        return amount

class StudentDiscount(DiscountPolicy):
    def apply_discount(self, amount: float) -> float:
        return amount * 0.9

class VipDiscount(DiscountPolicy):
    def apply_discount(self, amount: float) -> float:
        return amount * 0.8

@dataclass
class DiscountCalculator:
    policy: DiscountPolicy

    # теперь discount не зависит от пользователя
    def calculate(self, amount: float) -> float:
        return self.policy.apply_discount(amount)

calc = DiscountCalculator(NoDiscount())
print(calc.calculate(1.5))