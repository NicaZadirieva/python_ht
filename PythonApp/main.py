"""Dependency Inversion Principle"""

"""
Модули верхних уровней не должны напрямую зависеть от модулей нижних уровней.
Оба типа модулей должны зависеть от абстракций, а не абстракции от деталей.
"""

from dataclasses import dataclass
from abc import ABC, abstractmethod

class Logger(ABC):
    @abstractmethod
    def log(self, message: str):
       pass

class FileLogger(Logger):
    def log(self, message: str):
        print(f"Запись в файл: {message}")

class ConsoleLogger(Logger):
    def log(self, message: str):
        print(f"Запись в консоль: {message}")

@dataclass
class UserService:
    logger: Logger

    def create_user(self, name: str):
        self.logger.log(f"Создан аккаунт {name}")