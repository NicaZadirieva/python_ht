class Rectangle:
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    @property
    def area(self):
        """Площадь"""
        return self.width * self.height

rect = Rectangle(10, 5)
print(rect.area)