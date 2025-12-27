def log_decorator(func):
    def wrapper():
        print("func starting")
        func()
        print("func ended")
    return wrapper

@log_decorator
def say_hello():
    print("Hello")

say_hello()
