from dataclasses import dataclass
from typing import Dict

from models.lesson_model import Lesson

@dataclass
class Student:
    """
    Студент
    """
    name: str