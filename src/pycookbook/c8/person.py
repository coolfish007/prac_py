class Person:
    def __init__(self, first_name):
        """ 对first_name的访问即调用setter """
        self.first_name = first_name

    @property
    def first_name(self):
        """ 存储实际属性的名称_first_name没有特殊规定,按习惯前面加_. """
        print("=====>读取实例属性")
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        """ 如果不实现setter,first_name是只读属性. """
        print("=====>设置实例属性")
        if not isinstance(value, str):
            raise TypeError("Expected a string")
        self._first_name = value

    @first_name.deleter
    def first_name(self):
        raise AttributeError("Cannot delete attribute.")
