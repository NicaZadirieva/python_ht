"""Single Responsibility Principle"""
""""Класс должен иметь только одну причину для изменения, то есть он должен выполнять лишь одну функцию."""

from dataclasses import dataclass

@dataclass
class Order:
    items: list[str]

    def calculate_total(self):
        return len(self.items) * 10

    # не относится к Order
    def save_to_db(self):
        print("Сохранение в базу")

    # не относится к Order
    def send_confirmation_email(self):
        print("Отправка письма")