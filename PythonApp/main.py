from functools import wraps


class LimitCalls:
    def __init__(self, times: int):
        self.times = times

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if self.times <= 0:
                raise RuntimeError("Not valid invoking")
            self.times -= 1
            return func(*args, **kwargs)
        
        return wrapper


class Engine:
    @LimitCalls(3)
    def start(self):
        print("Двигатель запущен")


car = Engine()
car.start()
car.start()
car.start()

car.start() # RuntimeError