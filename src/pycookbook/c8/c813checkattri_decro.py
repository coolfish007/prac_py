import logging
from functools import partial
from pycookbook.c8.c813checkattri import Descriptor


def typed(expected_type, cls=None):
    if cls is None:
        # return lambda cls: typed(expected_type, cls)  # 这个地方可以用partial
        return partial(typed, expected_type)
    # 按mro链找__set__方法.
    super_set = cls.__set__

    def __set__(self, instance, value):
        if not isinstance(value, expected_type):
            logging.info(">====expected_type" + str(expected_type))
            raise TypeError("expected: " + str(expected_type))
        super_set(self, instance, value)

    cls.__set__ = __set__
    # 返回被decro的cls
    return cls


def unsigned(cls):
    super_set = cls.__set__

    def __set__(self, instance, value):
        if value < 0:
            raise ValueError("Expected >=0 ")
        super_set(self, instance, value)

    cls.__set__ = __set__
    return cls


@typed(int)
class Integer(Descriptor):
    pass


@unsigned
class UnsignedI1(Integer):
    """ 利用继承的mro进行多重检查后进行类的属性值设定.
    会先进行unsigned的检查,再进行typed的检查"""

    pass


@typed(int)
@unsigned
class UnsignedI2(Descriptor):
    """ 显式的使用多个装饰器进行多次检查,
    typed在外层,会先进行typed的检查."""

    pass
