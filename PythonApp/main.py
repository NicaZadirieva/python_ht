from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    id: int
    name: str
    email: str

def get_user_by_id(user_id: int) -> Optional[User]:
    users = [
        User(1, "Anton", "a@a.ru"),
        User(2, "Vasya", "v@v.ru"),
    ]

    for user in users:
        if user.id == user_id:
            return user

    return None

get_user_by_id(999)