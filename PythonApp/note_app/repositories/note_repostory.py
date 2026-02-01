"""
Хранение заметок
"""

from pathlib import Path
from note_app.domain import Note
from note_app.repositories.base_note_repository import BaseNoteRepository


class NoteRepository(BaseNoteRepository):
    """
    Класс для хранения заметок
    """

    def __init__(self, base_path: Path) -> None:
        self.base_path = base_path.resolve()

    def __check_path__(self, path: Path):
        """
        Базовая проверка пути
        """
        if not path.exists() or not path.is_dir():
            raise ValueError(f"Note doesn't exist: {path}")
        if self.base_path not in path.parents and path != self.base_path:
            raise ValueError("Access outside data directory is not allowed")
        return path

    def get_notes_by_path(self, path: Path) -> list[Note]:
        path = path.resolve()
        path = self.__check_path__(path)
        notes: list[Note] = []

        for sub_path in path.iterdir():
            if (
                sub_path.is_file()
                and not sub_path.name.startswith(".")
                and sub_path.suffix == ".md"
            ):
                notes.append(Note(name=sub_path.name, path=sub_path))
        return sorted(notes, key=lambda f: f.name)

    def create_note(self, path: Path, name: str) -> Note:
        path = path.resolve()
        path = self.__check_path__(path)
        if not name or "/" in name or "\\" in name:
            raise ValueError("Invalid note name")
        if name.startswith(".") or path.name.startswith("."):
            raise ValueError("Secret dirs is not allowed")
        path.mkdir(parents=True, exist_ok=False)
        return Note(path=path, name=name)

    def delete_note(self, note: Note) -> None:
        path = note.path.resolve()
        path = self.__check_path__(path)
        path.unlink()
