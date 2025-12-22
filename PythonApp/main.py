class User:
    """Пользователь"""
    users = [] # свойство класса

    def __init__(self, name):
        self.name = name
        User.users.append(self)

    @classmethod
    def total_users(cls):
        """Число пользователей"""
        return len(cls.users)

vasya = User("Вася")
kate = User("Катя")

print(User.total_users())