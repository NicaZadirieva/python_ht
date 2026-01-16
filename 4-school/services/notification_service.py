from abc import ABC, abstractmethod
from dataclasses import dataclass

class INotificationService(ABC):
    """
    Интерфейс для работы с уведомлениями
    """
    @abstractmethod
    def notify(self, event: str):
        """Уведомить пользователя о событии"""
        pass


class ConsoleNotificationService(INotificationService):
    """
    Консольный вывод уведомления
    """
    def notify(self, event: str):
        print(f"{event}")