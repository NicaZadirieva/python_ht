from dataclasses import Field, dataclass, field
from abc import ABC, abstractmethod
from typing import Dict
from models.student_model import Student
from models.lesson_model import Lesson

class IJournalRepository(ABC):
    """
    Интерфейс для работы с журналом
    """
    @abstractmethod
    def add_student(self, student: Student) -> Student:
        """
        Добавление студента
        """
        pass

    @abstractmethod
    def add_lesson(self, lesson: Lesson) -> Lesson:
        """
        Добавление урока
        """
        pass

    @abstractmethod
    def add_student_score(self, student: Student, lesson: Lesson, score: float) -> float:
        """
        Добавление оценки студента по предмету
        """
        pass

    @abstractmethod
    def get_student_scores(self, student: Student) -> Dict[Lesson, float]:
        """
        Получение оценок студента
        """
        pass

    @abstractmethod
    def find__student(self, student_name: str) -> Student:
        """
        Поиск студента по имени
        """
        pass

    @abstractmethod
    def find__lesson(self, lesson_name: str) -> Lesson:
        """
        Поиск урока по имени
        """
        pass

    @abstractmethod
    def get_lessons_count(self) -> int:
        """
        Получение количества уроков
        """
        pass

    @abstractmethod
    def get_students(self) -> list[Student]:
        """
        Получение всех студентов
        """
        pass

    @abstractmethod
    def get_lessons(self) -> list[Lesson]:
        """
        Получение всех уроков
        """
        pass

@dataclass
class InMemoryJournalRepo(IJournalRepository):
    """
    Работа с журналом в памяти
    """
    _students: list[Student] = field(default_factory=list)
    _lessons: list[Lesson] = field(default_factory=list)
    _scores: Dict[Student, Dict[Lesson, float]] = field(default_factory=dict)

    def add_student(self, student: Student):
        self._students.append(student)
        self._scores[student] = {}
        return student
    
    def add_lesson(self, lesson: Lesson):
        self._lessons.append(lesson)
        return lesson

    def add_student_score(self, student: Student, lesson: Lesson, score: float):
        self._scores[student][lesson] = score
        return score

    def find__student(self, student_name: str):
        for student in self._students:
            if student.name == student_name:
                return student
        return None

    def find__lesson(self, lesson_name: str):
        for lesson in self._lessons:
            if lesson.name == lesson_name:
                return lesson
        return None

    def get_student_scores(self, student: Student):
        return self._scores[student]

    def get_lessons_count(self):
        return len(self._lessons)

    def get_students(self) -> list[Student]:
        return self._students

    def get_lessons(self) -> list[Lesson]:
        return self._lessons