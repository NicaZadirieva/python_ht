"""Liskov substitution principle"""
"""Прицнип подстановки Барбары Лисков"""

"""Объекты дочерних классов должны быть взаимозаменяемы с объектами базовых классов без нарушения работы программы."""

from dataclasses import dataclass

@dataclass
class Payment():
    total_amount: int = 0

    def pay(self, amount: int):
        if amount > self.total_amount:
            raise ValueError("Значение amount > суммы в кошельке")
        self.total_amount -= amount
        return self.total_amount


@dataclass
class BonusPayment(Payment):
    bonuses: int = 0
    def pay(self, amount: int):
        if amount + self.bonuses > self.total_amount:
            raise ValueError("Значение amount + bonuses > суммы в кошельке")
        self.total_amount -= amount + self.bonuses
        return self.total_amount


@dataclass
class InstallmentPayment(Payment):
    n: int = 1
    def pay(self, amount: int):
        if self.n == 0:
            print("Рассрочка оплачена")
            return self.total_amount

        amount_with_n = amount / self.n
        if amount_with_n > self.total_amount:
            raise ValueError("Значение amount > суммы в кошельке")

        self.total_amount -= amount_with_n
        self.n -= 1

        return self.total_amount


payment = Payment(100)
bonusPayment = BonusPayment(100, 11)
installmentPayment = InstallmentPayment(100, 10)

print(f"Simple payment: {payment.pay(99)}")
print(f"Bonus payment: {bonusPayment.pay(1)}")
print(f"Install payment: {installmentPayment.pay(99)}")