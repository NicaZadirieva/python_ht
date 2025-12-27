from functools import wraps

def limit_calls(times: int):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            current_counter = getattr(self, "count_attr_" + func.__name__, 0)
            if current_counter >= times:
                raise RuntimeError("Not valid invoking")
            setattr(self, "count_attr_" + func.__name__, current_counter + 1)
            return func(self, *args, **kwargs)
        return wrapper
    return decorator



class Engine:
    @limit_calls(3)
    def start(self):
        print("Двигатель запущен")


car = Engine()
car.start()
car.start()
car.start()

car.start() # RuntimeError