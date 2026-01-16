from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Dict
from models import Student, Lesson

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
        NB!: can throw Exception
        """
        pass



class InMemoryJournalRepo(IJournalRepository):
    """
    Работа с журналом в памяти
    """
    _students: list[Student]
    _lessons: list[Lesson]
    _scores: Dict[Student, Dict[Lesson, float]]

    def add_student(self, student: Student):
        self._students.append(student)
        self._scores[student] = {}
        return student
    
    def add_lesson(self, lesson: Lesson):
        self._lessons.append(lesson)
        return lesson

    def __find__student(self, student_name: str):
        for student in self._students:
            if student.name == student_name:
                return student
        return None

    def __find__lesson(self, lesson_name: str):
        for lesson in self._lessons:
            if lesson.name == lesson_name:
                return lesson
        return None

    def add_student_score(self, student_name: str, lesson_name: str, score: float):
        student = self.__find__student(student_name)
        lesson = self.__find__lesson(lesson_name)

        if student is None or lesson is None:
            raise ValueError(f"Проверьте данные: студент {student.name} или урок {lesson.name} не найдены")
        else:
            self._scores[student][lesson] = score
            return score