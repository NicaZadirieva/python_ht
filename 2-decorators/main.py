def limit_args(max_value: int, mode: str):
    """Декоратор для ограничения числовых аргументов функции."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            args_result = []
            for arg in args:
                if arg > max_value:
                    if mode == "clip":
                        args_result.append(max_value)
                    elif mode == "error":
                        raise ValueError("превышение max_value")
                    else:
                        raise TypeError("Нет допустимого mode")
                else:
                    args_result.append(arg)
            kwargs_result = {}
            for (key, value) in kwargs.items():
                if value > max_value:
                    if mode == "clip":
                        kwargs_result[key] = max_value
                    elif mode == "error":
                        raise ValueError("превышение max_value")
                    else:
                        raise TypeError("Нет допустимого mode")
                else:
                    kwargs_result[key] = value
            return func(*args_result, **kwargs_result)
        return wrapper
    return decorator

@limit_args(max_value=10, mode="clip")
def multiply(a, b):
    return a * b

print(multiply(2, 3))
print(multiply(100, 3))
