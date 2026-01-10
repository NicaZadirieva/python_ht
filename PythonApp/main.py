"""Создать два типа хранилищ данных: в памяти (memory storage) и в файле (file storage)."""
from dataclasses import dataclass
from typing import Protocol

class Storage(Protocol):
    """Протокол для хранилища данных"""

    def save(self, data: str) -> None: ...
    def load(self) -> str: ...

@dataclass
class MemoryStorage(Storage):
    """Хранит данные в памяти"""
    storage_data: str = ""
    def save(self, data: str) -> None:
        self.storage_data = data

    def load(self) -> str:
        return self.storage_data



@dataclass
class FileStorage(Storage):
    """Хранит данные в файле"""
    file_name: str
    def save(self, data: str) -> None:
        with open(self.file_name, 'w', encoding="utf-8") as file:
            file.write(data)

    def load(self) -> str:
        with open(self.file_name, 'r', encoding="utf-8") as file:
            return file.read()


def use_storage(storage: Storage, data: str):
    storage.save(data)
    return storage.load()

mem = MemoryStorage()
file = FileStorage("file.txt")

user_input = input("Введите данные: ")
print(use_storage(mem, user_input))
print(use_storage(file, user_input))