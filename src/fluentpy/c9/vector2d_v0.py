from array import array
import math


class Vector2d:
    typecode = "d"

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __iter__(self):
        return (i for i in (self.x, self.y))

    def __repr__(self):
        class_name = type(self).__name__
        # {!r}会用repr()调用*self分量(即x,y),!s使用str()调用*self的分量
        # *self归功于__iter__()
        return "{}({!r},{!r})".format(class_name, *self)

    def __str__(self):
        # tuple(self)归功于__iter__()
        return str(tuple(self))

    def __byte__(self):
        return bytes([ord(self.typecode)]) + bytes(array(self.typecode, self))

    def __eq__(self, o: object) -> bool:
        return tuple(self) == tuple(o)

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self))
