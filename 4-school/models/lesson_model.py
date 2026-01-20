from dataclasses import dataclass

@dataclass
class Lesson:
    """
        Предмет изучения
    """
    name: str

    def __hash__(self):
        return hash((self.name))

    def __eq__(self, other):
        if not isinstance(other, Lesson):
            return False
        return self.name == other.name