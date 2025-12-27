from functools import wraps

def limit_calls(times: int):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            current_counter = 0
            if not hasattr(self, "count_attr_" + func.__name__):
                setattr(self, "count_attr_" + func.__name__, current_counter + 1)
            else:
                current_counter = getattr(self, "count_attr_" + func.__name__)
                setattr(self, "count_attr_" + func.__name__, current_counter + 1)
            if current_counter + 1 >= times:
                raise RuntimeError("Not valid invoking")
            else:
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