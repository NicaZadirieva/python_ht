"""
Хранение заметок
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional
from note_app.domain import Note


class BaseNoteRepository(ABC):
    """
    Базовый класс для хранения заметок
    """

    @abstractmethod
    def get_notes_by_path(self, path: Path) -> list[Note]:
        """
        Получение заметок по пути
        """

    @abstractmethod
    def create_note(self, path: Path, name: str, content: str = "") -> Note:
        """
        Создание заметки
        """

    @abstractmethod
    def delete_note(self, note: Note) -> None:
        """
        Удаление заметки
        """

    @abstractmethod
    def update_note(
        self, note: Note, content: str, new_name: Optional[str] = None
    ) -> Note:
        """Обновление заметки"""

    @abstractmethod
    def load_note(self, path: Path) -> Note:
        """
        Загрузка заметки
        """
