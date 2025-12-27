from functools import wraps

def log_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Log {func.__qualname__} {args} {kwargs}")
        return func(*args, **kwargs)
    return wrapper

class Service:
    @log_call
    def process(self, x: float) -> float:
        return x * 2

s = Service()

def a():
    return 1

print(a.__name__)

print(s.process.__name__)