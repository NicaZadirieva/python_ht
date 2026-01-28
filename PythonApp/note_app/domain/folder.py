"""
Обработка папок
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Folder:
    """
    Сущность папка
    """

    name: str
    path: Path

    def __post_init__(self) -> None:
        if not self.name or self.name.strip() == "":
            raise ValueError("Folder must have name")
