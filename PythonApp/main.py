from functools import wraps


class LimitCalls:
    def __init__(self, times: int):
        self.times = times

    def __call__(self, func):
        @wraps(func)
        def wrapper(self_obj, *args, **kwargs):
            attr_name = "count_attr_" + func.__name__
            current_counter = getattr(self_obj, attr_name, 0)
            
            if current_counter >= self.times:
                raise RuntimeError("Not valid invoking")
            
            setattr(self_obj, attr_name, current_counter + 1)
            return func(self_obj, *args, **kwargs)
        
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