"""
Описание задачи
Нужно создать универсальную функцию HandleEvent(), которая принимает различные типы пользовательских событий в интерфейсе и возвращает строку с информацией о событии.

Типы событий
ClickEvent:
Параметры: координаты x и y (оба типа int).
KeyEvent:
Параметр: кнопка key (типа str).
ResizeEvent:
Параметры: width и height (оба типа int).
Реализация функции HandleEvent()
Описание событий через классы:
Создаём data-классы для каждого типа события:
ClickEvent с полями x и y.
KeyEvent с полем key.
ResizeEvent с полями width и height.
Обработка событий:
Используем конструкцию match-case для различения типов событий:
ClickEvent: извлечь x и y, вернуть строку f"Clicked at x={x}, y={y}".
KeyEvent: извлечь key, вернуть строку f"Key pressed: {key}".
ResizeEvent: извлечь width и height, вернуть строку f"Resized to {width}x{height}".
Если событие неизвестно, возбудить ошибку ValueError.
Преимущества:
Использование match-case делает код более читаемым и позволяет избежать ряда if-else.
Обработка исключений через ValueError позволяет легко идентифицировать неподдерживаемые события.
Тестирование
Тестируем функцию HandleEvent() на следующих примерах событий:
ClickEvent(1, 10)
KeyEvent("Enter")
ResizeEvent(1920, 1080)
Проверяем, что функция возвращает корректные строки для каждого из событий, подтверждая правильность работы кода.
"""
from dataclasses import dataclass
from typing import TypeVar

@dataclass
class ClickEvent:
    x: int
    y: int

@dataclass
class KeyEvent:
    key: str

@dataclass
class ResizeEvent:
    width: float
    height: float

Event = TypeVar("Event", ClickEvent, KeyEvent, ResizeEvent)

def handleEvent(event: Event) -> str:
    match event:
        case ClickEvent(x = x, y = y):
            return f"Clicked at x={x}, y={y}"
        case KeyEvent(key = key):
            return f"Key pressed: {key}"
        case ResizeEvent(width = width, height = height):
            return f"Resized to {width}x{height}"
        case _:
            raise ValueError("Invalid error")


eveClick = ClickEvent(1, 10)
eveKey = KeyEvent("Enter")
eveResize = ResizeEvent(1920, 1080)

print(handleEvent(eveClick))
print(handleEvent(eveKey))
print(handleEvent(eveResize))