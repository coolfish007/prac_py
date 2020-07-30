import types
from functools import wraps


class Profiled:
    def __init__(self, func):
        f = wraps(func)
        print(f"in __init__(),wraps(func)->{f}")
        print("*" * 10)
        print("self:", self)
        print("*" * 10)
        f = f(self)
        print(f"in __init__(),f(self)->{f}")
        self.ncalls = 0

    def __call__(self, *args, **kwargs):
        print("in __call__()...")
        self.ncalls += 1
        print("ncalls:...", self.ncalls)

        return self.__wrapped__(*args, **kwargs)

