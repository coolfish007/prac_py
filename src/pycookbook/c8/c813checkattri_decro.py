from pycookbook.c8.c813checkattri import Descriptor


def Typed(expectd_type, cls=None):
    if cls is None:
        return lambda cls: Typed(expectd_type, cls)
    # 按mro链找__set__方法.
    super_set = cls.__set__

    def __set__(self, instance, value):
        if not isinstance(value, expectd_type):
            raise TypeError("expected: " + str(expectd_type))
        super_set(self, instance, value)

    cls.__set__ = __set__
    # 返回被decro的cls
    return cls
