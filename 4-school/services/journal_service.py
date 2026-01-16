from dataclasses import dataclass
from typing import Dict

from repositories.journal_repo import IJournalRepository
from models.student_model import Student
from models.lesson_model import Lesson
from services.notification_service import INotificationService

@dataclass
class JournalService:
    """
    Сервис для работы с журналом
    """
    repo: IJournalRepository
    notificationService: INotificationService

    def add_student(self, student_name: str) -> Student:
        """
        Добавление студента
        """
        student = Student(student_name)
        return self.repo.add_student(student)

    def add_lesson(self, lesson_name: str) -> Lesson:
        """
        Добавление урока
        """
        lesson = Lesson(lesson_name)
        return self.repo.add_lesson(lesson)

    def __calc_average_score__(self, scores: Dict[Lesson, float], lessons_count: int) -> float:
        total = sum(scores.values())
        return total / lessons_count

    def add_student_score(self, student_name: str, lesson_name: str, score: float) -> float:
        """
        Добавление оценки студента по предмету
        NB!: can throw Exception
        """
        student = self.repo.find__student(student_name)
        lesson = self.repo.find__lesson(lesson_name)

        if student is None or lesson is None:
            raise ValueError(f"Студент или урок не найден")

        score = self.repo.add_student_score(student, lesson, score)
        scores = self.repo.get_student_scores(student)
        lessons_count = self.repo.get_lessons_count()

        if self.__calc_average_score__(scores, lessons_count) < 3.5:
            self.notificationService.notify(f"Обратите внимание! {student.name} имеет проблемы с успеваемостью")

        return score