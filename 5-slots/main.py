from dataclasses import dataclass



@dataclass
class User:
    name: str
    email: str
    password: str

@dataclass
class SlotUser:
    __slots__=('name', 'email', 'password')
    name: str
    email: str
    password: str

# Создаем списки
users_list = []
slot_users_list = []

for i in range(100000):
    # Создаем User
    user = User(
        name=f"User_{i}",
        email=f"user_{i}@example.com",
        password=f"password_{i}"
    )
    users_list.append(user)
    
    # Создаем SlotUser с теми же данными
    slot_user = SlotUser(
        name=f"User_{i}",
        email=f"user_{i}@example.com",
        password=f"password_{i}"
    )
    slot_users_list.append(slot_user)


