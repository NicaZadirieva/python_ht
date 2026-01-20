from dataclasses import dataclass
import sys


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

# Измеряем размер одного объекта
def estimate_object_size(obj):
    """Приблизительная оценка размера объекта"""
    total = sys.getsizeof(obj)
    
    if hasattr(obj, '__dict__'):
        # Для обычного User добавляем размер __dict__ и его содержимого
        total += sys.getsizeof(obj.__dict__)
        for key, value in obj.__dict__.items():
            total += sys.getsizeof(key) + sys.getsizeof(value)
    elif hasattr(obj, '__slots__'):
        # Для SlotUser добавляем размер атрибутов
        for attr_name in obj.__slots__:
            total += sys.getsizeof(getattr(obj, attr_name))
    
    return total

# Размер одного элемента
user_single_size = estimate_object_size(users_list[0])
slot_user_single_size = estimate_object_size(slot_users_list[0])

print("1. Размер одного элемента:")
print(f"   User: ~{user_single_size:,} байт")
print(f"   SlotUser: ~{slot_user_single_size:,} байт")
print(f"   Экономия на одном объекте: {user_single_size - slot_user_single_size:,} байт")
print()

# Оценка общего размера
print("2. Оценка общего размера списков:")
print(f"   Список User: ~{(sys.getsizeof(users_list) + user_single_size * len(users_list)):,} байт")
print(f"   Список SlotUser: ~{(sys.getsizeof(slot_users_list) + slot_user_single_size * len(slot_users_list)):,} байт")
print()


