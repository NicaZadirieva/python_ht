"""
Работа с репозиторием для папок
"""

from pathlib import Path

from note_app.domain import Folder
from note_app.repositories.base_folder_repository import BaseFolderRepository


class FolderRepository(BaseFolderRepository):
    """
    Класс для репозитория с папками
    """
    def __init__(self, base_path: Path) -> None:
        self.base_path = base_path.resolve()

    def get_folders_by_path(self, path: Path) -> list[Folder]:
        path = path.resolve()
        if not path.exists() or not path.is_dir():
            raise ValueError(f"Folder doesn't exist: {path}")
        if self.base_path not in path.parents and path != self.base_path:
            raise ValueError("Access outside data directory is not allowed")
        folders: list[Folder] = []
        
        for sub_path in path.iterdir():
            if sub_path.is_dir() and not sub_path.name.startswith("."):
                folders.append(
                    Folder(
                        name=sub_path.name,
                        path = sub_path
					)
				)
        return sorted(folders, key = lambda f: f.name)

    def create_folder(self, name: str) -> Folder:



    def delete_folder(self, name: str) -> None:

