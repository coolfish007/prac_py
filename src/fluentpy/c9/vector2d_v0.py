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
        # 等同与pycb C8.1的
        # return '{0}({0.x!r},{0.y!r})'.fromat(class_name,*self)
        return "{}({!r},{!r})".format(class_name, *self)

    def __str__(self):
        # tuple(self)归功于__iter__()
        return str(tuple(self))

    def __bytes__(self):
        print("*" * 5, "in __bytes__()")
        return bytes([ord(self.typecode)]) + bytes(array(self.typecode, self))

    def __eq__(self, o: object) -> bool:
        return tuple(self) == tuple(o)

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self))

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(*memv)
