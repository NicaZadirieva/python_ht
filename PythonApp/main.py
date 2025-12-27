def log_call(func):
    def wrapper(*args, **kwargs):
        print(f"Log {func.__qualname__} {args} {kwargs}")
        return func(*args, **kwargs)
    return wrapper

class Service:
    @log_call
    def process(self, x: float) -> float:
        return x * 2

Service().process(5)