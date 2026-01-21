"""
save_get:
Цель: Получение значения из списка по индексу с безопасной обработкой.
Описание: Функция принимает список (list[T]) и индекс (int).
Возврат: Возвращает элемент списка (T) или None, если индекс за пределами списка.
Используемые методы: Optional[T] для возврата либо значения, либо None.
map_optional:
Цель: Применение функции к значению, если оно не None.
Описание: Функция принимает значение (Optional[T]) и трансформер- функцию (Callable[[T], R]).
Возврат: Возвращает преобразованное значение (Optional[R]), либо None, если исходное значение было None.
Используемые методы: Optional, Callable, два дженерика для типизации входного и выходного типов.
or_else:
Цель: Возврат значения, если оно не None, или дефолтного значения в противном случае.
Описание: Функция принимает значение (Optional[T]) и дефолтное значение (T).
Возврат: Возвращает значение (T), либо дефолтное, если основное значение None.
"""
from typing import TypeVar, Optional, Callable

T = TypeVar("T")
R = TypeVar("R")

def save_get(arr: list[T], i: int) -> Optional[T]:
    return None if len(arr) <= i else arr[i]

def map_optional(a: Optional[T], callback: Callable[[T], R]) -> Optional[R]:
    if a == None:
        return None
    return callback(a)

def or_else(a: Optional[T], default: T) -> T:
    return default if a is None else a

arr = [1, 2, 3]
print(save_get(arr, 4))

print([map_optional(a, str) for a in arr])

print(or_else(save_get(arr, 4), "default"))
