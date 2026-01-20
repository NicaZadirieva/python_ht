from abc import ABC, abstractmethod
from dataclasses import dataclass

from models.lesson_model import Lesson
from repositories.journal_repo import IJournalRepository
from models.student_model import Student

class IStatisticsService(ABC):
    """
    Интерфейс для работы со статистикой
    """
    @abstractmethod
    def print_stat(self) -> None:
        """
        Печатать статистику
        """
        pass

@dataclass
class ScoreStatistics(IStatisticsService):
    """
    Статистика по оценкам
    """
    journalRepo: IJournalRepository 

    def __calc_average_score_by_student__(self, student: Student) -> float:
        scores = self.journalRepo.get_student_scores(student)
        lessons_count = self.journalRepo.get_lessons_count()
        return sum(scores.values()) / lessons_count

    def __calc_average_score_by_lesson__(self, lesson: Lesson) -> float:
        students = self.journalRepo.get_students()
        total = 0
        total_count = 0
        for student in students:
            scores = self.journalRepo.get_student_scores(student)
            if lesson in scores.keys():
                total += scores[lesson]
                total_count += 1
        return 0 if total_count == 0 else total / total_count

    def print_stat(self) -> None:
        students = self.journalRepo.get_students()
        lessons = self.journalRepo.get_lessons()

        print("Статистика по студентам: ")
        for student in students:
            average_score_by_student = self.__calc_average_score_by_student__(student)
            print(f"Средник балл {student.name}: {average_score_by_student}")

        print("Статистика по урокам: ")
        for lesson in lessons:
            average_score_by_lesson = self.__calc_average_score_by_lesson__(lesson)
            print(f"Средний балл {lesson.name}: {average_score_by_lesson}")
        