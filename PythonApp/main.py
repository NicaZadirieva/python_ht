import random


def retry(max_times: int):
    def decorator(func):
        def wrapper(*args, **kwargs):
            is_success = True
            for _ in range(max_times - 1):
                try:
                    return func(*args, **kwargs)
                except:
                     is_success = False
            if not is_success:
                return func(*args, **kwargs)
        return wrapper
    return decorator

@retry(7)
def unstable():
    if random.random() < 0.7:
        raise ValueError("Ошибка соединения")
    print("Успешное соединение")

unstable()