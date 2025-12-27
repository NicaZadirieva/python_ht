def say_hello():
    print("Hello")

def log_decorator(func):
    def wrapper():
        print("func starting")
        func()
        print("func ended")
    return wrapper

decorated = log_decorator(say_hello)

decorated()