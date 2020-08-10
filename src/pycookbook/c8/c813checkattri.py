import logging

from pycookbook.c9.loggeds import loggeds

# logging.basicConfig(level=logging.DEBUG)


class Descriptor:
    def __init__(self, name=None, **opts):
        logging.debug("=>init in Descriptor.")
        self.name = name
        for k, v in opts.items():
            setattr(self, k, v)

    @loggeds
    def __set__(self, ins, value):
        logging.debug("=>set in Descriptor.")
        ins.__dict__[self.name] = value
        logging.debug("=>set in Descriptor end.")


class Typed(Descriptor):
    expected_type = type(None)

    def __set__(self, ins, value):
        logging.debug("=>set in Typed.")
        if not isinstance(value, self.expected_type):
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
