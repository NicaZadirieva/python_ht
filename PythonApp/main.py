from typing import TypeGuard


def is_int_list(x: list[int] | list[str]) -> TypeGuard[list[int]]:
    return all(isinstance(i, int) for i in x)

def is_str_list(x: list[int] | list[str]) -> TypeGuard[list[str]]:
    return all(isinstance(i, str) for i in x)

def f(xs: list[int] | list[str]):
    if is_int_list(xs):
        xs[0].is_integer()
    if is_str_list(xs):
        xs[0].capitalize()