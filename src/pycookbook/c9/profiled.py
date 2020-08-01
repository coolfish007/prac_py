import types
from functools import wraps


class Profiled:
    def __init__(self, func):
        """ 传入func主要目的就是使用wraps(func)把func的属性传入Profiled的实例.
            如果不需要,则不用传入func,但__call__需要接收func以备调用并定义闭包. 
            带参数的装饰器类通常这么做,相当于创建对象后,将对象变为callable,传入func调用,同样__call__中定义闭包."""
        f = wraps(func)
        print(f"===1===in __init__(),wraps(func)->{f}")
        print(f"===2===self:{self}")
        f = f(self)
        print(f"===3===in __init__(),f(self)->{f}")
        self.ncalls = 0

    def __call__(self, *args, **kwargs):
        self.ncalls += 1
        print(f"===4===in __call__(),ncalls:...{self.ncalls}")

        return self.__wrapped__(*args, **kwargs)

    def __get__(parameter_list):
        pass
