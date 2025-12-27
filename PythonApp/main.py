import random


def retry(max_times: int):
    def decorator(func):
        def wrapper(*args, **kwargs):
            is_success = False
            for _ in range(max_times - 1):
                try:
                    func(*args, **kwargs)
                    is_success = True
                    break
                except:
                    pass
            if not is_success:
                func(*args, **kwargs)
        return wrapper
    return decorator

@retry(3)
def unstable():
    if random.random() < 0.7:
        raise ValueError("Ошибка соединения")
    print("Успешное соединение")

unstable()