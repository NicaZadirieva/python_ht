"""
Функция make_pair:
Задача: Принять два значения и создать из них кортеж (tuple).
Типизация: Используем дженерики T и R для обозначения типов входных значений и кортежа.
Функция get_first:
Задача: Извлечь первый элемент из переданного кортежа.
Типизация: Принимает кортеж (tuple) типов T и R, возвращает тип T.
Функция get_second:
Задача: Извлечь второй элемент из переданного кортежа.
Типизация: Принимает кортеж (tuple) типов T и R, возвращает тип R.
Функция swap_pairs:
Задача: Поменять местами элементы в переданном кортеже.
Типизация: Принимает кортеж (tuple) типов T и R, возвращает кортеж (tuple) типов R и T.
"""

from typing import TypeVar

T = TypeVar("T")
R = TypeVar("R")

def make_pair(a: T, b: R) -> tuple[T, R]:
    return (a, b)

def get_first(pair: tuple[T, R]) -> T:
    return pair[0]
    
def get_second(pair: tuple[T, R]) -> R:
    return pair[1]

def swap_pairs(pair: tuple[T, R]) -> tuple[R, T]:
    return (pair[1], pair[0])


t = make_pair(1, 2)
print(get_first(t))
print(get_second(t))

print(swap_pairs(t))