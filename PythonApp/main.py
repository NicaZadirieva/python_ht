def add_repr(cls):
    def __repr__(self):
        return f"{cls.__name__}[{self.__dict__}]"
    cls.__repr__ = __repr__
    return cls

@add_repr
class User:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age


# User = decorator(User)
user = User("Nica", 25)
print(user)