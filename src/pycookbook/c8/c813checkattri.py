import logging

from pycookbook.c9.loggeds import loggeds


class Descriptor:
    def __init__(self, name=None, **opts):
        logging.debug("=>init in Descriptor.")
        self.name = name
        for k, v in opts.items():
            setattr(self, k, v)

    # @loggeds
    # self:描述器本身的实例;ins:描述器所在的类的实例;value:实例的属性值.
    def __set__(self, ins, value):
        logging.debug("=>set in Descriptor.")
        ins.__dict__[self.name] = value
        logging.debug("=>set in Descriptor end.")


class Typed(Descriptor):
    expected_type = type(None)

    def __set__(self, ins, value):
        logging.debug("=>set in Typed.")
        if not isinstance(value, self.expected_type):
            # TODO:str(self.expected_type)没有打印出来
            raise TypeError("expected " + str(self.expected_type))
        super().__set__(ins, value)  # 按mro链执行Typed后的一个.
        logging.debug("=>set in Typed end.")


class Unsigned(Descriptor):
    def __set__(self, ins, value):
        if value < 0:
            raise ValueError("Expected >=0")
        super().__set__(ins, value)


class MaxSized(Descriptor):
    def __init__(self, name=None, **opts):
        logging.debug("=>init in MaxSized.")
        if "size" not in opts:
            raise TypeError("missing size option")
        super().__init__(name, **opts)

    def __set__(self, ins, value):
        logging.debug("=>set in MaxSized.")
        if len(value) >= self.size:
            raise ValueError("size must be < " + str(self.size))
        super().__set__(ins, value)
        logging.debug("=>set in MaxSized end.")


class Integer(Typed):
    expected_type = int


class UnsignedInteger(Integer, Unsigned):
    pass


class Float(Typed):
    expected_type = float


class UnsignedFloat(Float, Unsigned):
    pass


class String(Typed):
    expected_type = str


class SizedString(String, MaxSized):
    pass


def check_attri(**kwargs):
    def decorate(cls):
        for k, v in kwargs.items():
            logging.info(f"k={k},v={v}")
            logging.info(isinstance(v, Descriptor))
            if isinstance(v, Descriptor):
                logging.info(f"instance of Descriptor,v is {type(v)}")
                # SizedString(siz=...)已构造,name=None,需要设定.
                v.name = k
                setattr(cls, k, v)
            else:
                # 传入的是UnsignedInteger类名,不是UnsignedInteger()对象.
                # SizedString由于要传入参数,所以传入的是对象.
                logging.info(f"not instance of Descriptor,v is {type(v)}")
                # 用k构造一个Descriptor()对应子类的实例.k是name,没有其他的参数.
                setattr(cls, k, v(k))

        return cls

    return decorate
