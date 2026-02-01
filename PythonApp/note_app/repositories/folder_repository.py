"""
Работа с репозиторием для папок
"""

from pathlib import Path
import shutil

from note_app.domain import Folder
from note_app.repositories.base_folder_repository import BaseFolderRepository


class FolderRepository(BaseFolderRepository):
    """
    Класс для репозитория с папками
    """

    def __init__(self, base_path: Path) -> None:
        self.base_path = base_path.resolve()

    def __check_path__(self, path: Path):
        """
        Базовая проверка пути
        """
        if not path.exists() or not path.is_dir():
            raise ValueError(f"Folder doesn't exist: {path}")
        if self.base_path not in path.parents and path != self.base_path:
            raise ValueError("Access outside data directory is not allowed")
        return path

    def get_folders_by_path(self, path: Path) -> list[Folder]:
        path = path.resolve()
        path = self.__check_path__(path)
        folders: list[Folder] = []

        for sub_path in path.iterdir():
            if sub_path.is_dir() and not sub_path.name.startswith("."):
                folders.append(Folder(name=sub_path.name, path=sub_path))
        return sorted(folders, key=lambda f: f.name)

    def create_folder(self, path: Path, name: str) -> Folder:
        path = path.resolve()
        path = self.__check_path__(path)
        if not name or "/" in name or "\\" in name:
            raise ValueError("Invalid folder name")
        if name.startswith(".") or path.name.startswith("."):
            raise ValueError("Secret dirs is not allowed")
        path.mkdir(parents=True, exist_ok=False)
        return Folder(path=path, name=name)

    def delete_folder(self, folder: Folder) -> None:
        dir_to_delete = folder.path.resolve()
        dir_to_delete = self.__check_path__(dir_to_delete)
        if dir_to_delete == self.base_path:
            raise ValueError("Deleting base path is not allowed")
        shutil.rmtree(dir_to_delete)
