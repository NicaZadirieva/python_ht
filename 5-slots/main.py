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


