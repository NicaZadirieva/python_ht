"""Liskov substitution principle"""
"""Прицнип подстановки Барбары Лисков"""

"""Объекты дочерних классов должны быть взаимозаменяемы с объектами базовых классов без нарушения работы программы."""

from dataclasses import dataclass


@dataclass
class User:
    name: str
    bonus: int = 0

    def add_bonus(self, amount: int):
        self.bonus += amount
        print(f"Пользователь {self.name} получил {amount} бонусов. Всего {self.bonus} бонусов")


class PremiumUser(User):
    def add_bonus(self, amount: int):
        self.bonus += amount * 2
        print(f"Пользователь {self.name} получил {amount * 2} бонусов. Всего {self.bonus} бонусов")

# нарушение LSP.
class BannedUser(User):
    def add_bonus(self, amount: int):
        raise Exception("Юзер забанен")

user = User("Вася")

def reward_user(user: User):
    user.add_bonus(100)

reward_user(user)
reward_user(PremiumUser("Вася2"))
reward_user(BannedUser("Вася3"))