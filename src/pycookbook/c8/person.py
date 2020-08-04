class Person:
    def __init__(self, first_name):
        self.first_name = first_name

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        """ 如果不实现setter,first_name是只读属性. """
        if not isinstance(value, str):
            raise TypeError("Expected a string")
        self._first_name = value

    @first_name.deleter
    def first_name(self):
        raise AttributeError("Cannot delete attribute.")
