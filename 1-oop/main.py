"""Дз 1 по теме ООП"""

from dataclasses import dataclass, field


@dataclass
class BankAccount:
    """Банковский счет простого вида"""
    accountHolder: str
    accountId: str | int
    balance: float | int = 0

    accounts_created: int = field(init = False, default = 0)

    def __post_init__(self):
        if self.balance < 0:
            raise ValueError("Баланс должен быть положительным числом")
        BankAccount.accounts_created += 1


    def deposit(self, amount: float | int):
        """Пополнение счёта на сумму amount"""
        if amount < 0:
            raise ValueError("Баланс можно только пополнить")
        self.balance += amount

    def withdraw(self, amount: float | int):
        """Снятие денег со счёта. Нельзя уйти в минус."""
        if self.balance - amount < 0:
            raise ValueError("Недостаточно средств")
        self.balance -= amount

    def transfer_to(self, bankAccount, accountSum: int | float):
        """Перевод денег на другой счёт BankAccount"""
        if not isinstance(bankAccount, BankAccount):
            raise ValueError("Передать деньги можно только банковскому счету")
        if accountSum < 0:
            raise ValueError("Сумма перевода должна быть положительным числом")
        if self.account < accountSum:
            raise ValueError("Недостаточно средств")
        bankAccount.deposit(accountSum)
        self.withdraw(accountSum)

    def info(self):
        """Краткая информацией о счёте"""
        return f"BankAccount#{self.accountId} = ({self.accountHolder}, {self.balance})"

    @classmethod
    def get_accounts_created(cls):
        """Количество созданных счетов"""
        return cls.accounts_created