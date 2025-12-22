"""Демо модуль для курса"""

class User:
    """Пользователь системы"""
    email: str
    name: str
    age: int

print(type(User))
userMaria = User()

print(userMaria)

userAnton = User()
print(userAnton)

userAnton.email = "a@a.ru"