import math


def lazyproperty(func):
    name = "_lazy_" + func.__name__

    @property
    def lazy(self):
        print("=" * 5, ">lazy(self) 1>enter ")
        if hasattr(self, name):
            print("=" * 5, ">lazy(self) 2>has attr ", self, name)
            return getattr(self, name)
        else:
            print("=" * 5, ">lazy(self) 3>no attr ", self, name, func)
            print(
                "=" * 5,
                ">lazy(self) 4>func ",
                func,
                func.__code__.co_varnames,
                func.__code__.co_argcount,
            )
            # func是Circle.perimeter而不是Circle的实例.perimeter
            value = func(self)
            setattr(self, name, value)
            return value

    return lazy


class Circle:
    def __init__(self, radius) -> None:
        self.radius = radius

    @lazyproperty
    def area(self):
        print("=" * 5, ">area(self) 1>computing area")
        return math.pi * self.radius ** 2

    # @lazyproperty
    def perimeter(self):
        print("=" * 5, ">perimeter() 1>computing perimeter")
        return math.pi * self.radius * 2
