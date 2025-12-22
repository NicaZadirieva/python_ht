from datetime import date

class Book:
    """Книга"""
    def __init__(self, title: str, year: int):
        self.title = title
        self.year = year

    @staticmethod
    def years_since(year: int):
        """Сколько прошло лет после публикации любой книги"""
        return date.today().year - year


book = Book("Властелин колец", 1985)
print(Book.years_since(book.year))