"""Принцип открытости-закрытости"""
"""Классы должны быть открыты для расширения, но закрыты для модификации."""

# class Notifier:
#     def send(self, message: str, method: str) -> None:
#         if method == "email":
#             print(f"[Email] Отправлено сообщение: {message}")
#         elif method == "push":
#             print(f"[Push] Отправлено сообщение: {message}")
#         else:
#             print("Неизвестный способ уведомления")

from abc import ABC, abstractmethod
from dataclasses import dataclass

class Sender(ABC):
    """Общий класс для отправки данных"""
    @abstractmethod
    def send(self, message: str) -> None: 
        """Отправка данных"""
        pass

class EmailSender(Sender):
    """Отправка по email"""
    def send(self, message: str) -> None: 
        print(f"[Email] Отправлено сообщение: {message}")

class PushSender(Sender):
    """Отправка push-уведомления"""
    def send(self, message: str) -> None: 
        print(f"[Push] Отправлено сообщение: {message}")

@dataclass
class Notifier:
    sender : Sender
    def send(self, message: str):
        self.sender.send(message)


notifier = Notifier(EmailSender())
notifier.send("Привет")