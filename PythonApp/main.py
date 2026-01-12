"""Принцип открытости-закрытости"""
"""Классы должны быть открыты для расширения, но закрыты для модификации."""

class DiscountCalculator:
    """Нарушение принципа, так как может измениться логика user_type"""
    def calculate(self, user_type: str, amount: float) -> float:
        if user_type == "student":
            return amount * 0.9
        elif user_type == "vip":
            return amount * 0.8
        else:
            return amount