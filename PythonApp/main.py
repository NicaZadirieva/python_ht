def log(func):
    def wrapper(*args, **kwargs):
        print(f"Invoking {func.__name__} с аргументами {args} {kwargs}")
        result = func(*args, **kwargs)
        return result
    return wrapper

@log
def add(a: float, b: float):
    return a + b

print(add(3, 5))
