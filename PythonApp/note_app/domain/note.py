"""
Обработка заметок
"""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class Note:
    """
    Сущность заметка
    """

    name: str
    path: Path
    content: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    def __post_init__(self) -> None:
        if not self.name or self.name.strip() == "":
            raise ValueError("Note must have name")
