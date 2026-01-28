"""
Работа с репозиторием для папок
"""

from abc import ABC, abstractmethod
from pathlib import Path

from note_app.domain import Folder


class BaseFolderRepository(ABC):
    """
    Абстрактный класс для репозитория с папками
    """

    @abstractmethod
    def get_all_folders(self) -> list[Folder]:
        """Получить все папки"""

    @abstractmethod
    def get_all_folder_by_path(self, path: Path) -> Folder:
        """Получить папку по пути"""

    @abstractmethod
    def create_folder(self, name: str) -> Folder:
        """Создать папку"""

    @abstractmethod
    def delete_folder(self, name: str) -> None:
        """Удалить папку"""
