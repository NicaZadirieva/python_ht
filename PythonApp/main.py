class Course:
    """Базовый класс курса"""
    def __init__(self, price: int, name: str, duration_ms: int):
        self.__price = price
        self.name = name
        self.duration_ms = duration_ms

    def get_price(self):
        """Получение цены"""
        return self.__price

    def print_info(self):
        """Вывод информации о курсе"""
        print(f"{self.name}: {self.duration_ms}ms, {self.get_price()}rub")


class AiCourse(Course):
    """АИ и тренажеры"""
    def get_credit(self):
        """Расчет рассрочки"""
        credit = self.get_price() / self.duration_ms
        return credit

class ProjectCourse(Course):
    """Проектный курс"""
    def __init__(self, price: int, name: str, duration_ms: int, project_name: str):
        super().__init__(price, name, duration_ms)
        self.__project_name = project_name

    def print_info(self):
        """Вывод информации о курсе"""
        print(f"{self.name}, {self.__project_name}: {self.duration_ms}ms, {self.get_price()}rub")

    def get_credit(self):
        """Расчет рассрочки"""
        credit = self.get_price() / self.duration_ms
        return credit

    def get_project_info(self):
        """Информация о проекте"""
        return self.__project_name


