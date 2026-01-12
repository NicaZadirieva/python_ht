"""Dependency Inversion Principle"""

"""
Модули верхних уровней не должны напрямую зависеть от модулей нижних уровней.
Оба типа модулей должны зависеть от абстракций, а не абстракции от деталей.
"""

from dataclasses import dataclass


class FileLogger:
    def log(self, message: str):
        print(f"Запись в файл: {message}")

@dataclass
class UserService:
    logger = FileLogger() # нарушение DIP

    def create_user(self, name: str):
        self.logger.log(f"Создан аккаунт {name}")