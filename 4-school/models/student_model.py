from dataclasses import dataclass
from typing import Dict

from models.lesson_model import Lesson

@dataclass
class Student:
    """
    Студент
    """
    name: str

    def __hash__(self):
        return hash((self.name))

    def __eq__(self, other):
        if not isinstance(other, Student):
            return False
        return self.name == other.name