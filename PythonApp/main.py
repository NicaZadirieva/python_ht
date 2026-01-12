"""Single Responsibility Principle"""
""""Класс должен иметь только одну причину для изменения, то есть он должен выполнять лишь одну функцию."""
"""
Упражнение заключается в следующем:

Создание модели студента:

Студент имеет имя и оценку.
Реализация через data-класс.
Создание класса репозитория студентов:

Хранение списка студентов.
Методы для добавления нового студента и получения списка всех студентов.
Создание класса для статистики студентов:

Метод для расчета средней оценки.
Метод для нахождения студента с наилучшей оценкой.
Взаимодействие с репозиторием для получения данных.
Создание класса для печати отчета:

Генерация отчета с информацией о студенте, среднем балле и лучшем студенте.
Вывод всех студентов и их оценок.
Практическая реализация:

Создание экземпляров каждого из классов.
Добавление нескольких студентов в репозиторий.
Печать отчета с помощью созданного метода.
"""

from dataclasses import dataclass, field

@dataclass
class Student:
    """Модель студента"""
    name: str
    score: float

@dataclass
class StudentStorage:
    """Хранение списка студентов"""
    students: list[Student] = field(default_factory=list)

    def add_student(self, student: Student) -> Student:
        """Добавление нового студента"""
        self.students.append(student)
        return student

    def get_all_students(self) -> list[Student]:
        """Получение списка всех студентов"""
        return self.students

@dataclass
class StudentStatistics:
    """Статистика студентов"""
    studentStorage: StudentStorage

    def get_best_student(self):
        """Метод для нахождения студента с наилучшей оценкой"""
        students = self.studentStorage.get_all_students()
        best_student = students[0]
        for student in students:
            if student.score > best_student.score:
                best_student = student
        return best_student

    def get_average_score(self):
        """Метод для нахождения среднего балла"""
        students = self.studentStorage.get_all_students()
        sum_score = 0
        for student in students:
            sum_score += student.score
        return sum_score / len(students) if len(students) > 0 else 0 


@dataclass
class StudentReportService:
    """Печать отчета"""
    studentStatistics: StudentStatistics
    studentStorage: StudentStorage

    def generate_best(self) -> None:
        best_student = self.studentStatistics.get_best_student()
        print(f"Best student: {best_student.name} {best_student.score}")

    def generate_all(self) -> None:
        students = self.studentStorage.get_all_students()
        for student in students:
            print(f"Student: {student.name} {student.score}")

    def generate_average_score(self) -> None:
        print(f"Average score: {self.studentStatistics.get_average_score()}")

# пример использования
studentStorage = StudentStorage()
studentStatistics = StudentStatistics(studentStorage)
studentReportService = StudentReportService(studentStatistics, studentStorage)

studentStorage.add_student(
    Student(
        name="Вероника",
        score=3.5
    )
)

studentStorage.add_student(
    Student(
        name="Полечка",
        score=4.5
    )
)

studentReportService.generate_all()
studentReportService.generate_best()
studentReportService.generate_average_score()