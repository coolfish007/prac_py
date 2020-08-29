import weakref


class Singleton(type):
    def __init__(self, *args, **kwargs):
        print("in metaclass Singleton __init__()")
        self.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            self.__instance = super().__call__(*args, **kwargs)
            return self.__instance
        else:
            return self.__instance


class Cached(type):
    def __init__(self, *args, **kwargs):
        print("in metaclass Cached __init__()", args, kwargs)
        self.__cache = weakref.WeakValueDictionary()
        super().__init__(*args, **kwargs)  # 这个放在最前和最后有无区别?

    def __call__(self, *args, **kwargs):  # 这里的参数即初始化Spam3的参数.注意即使ids有默认值,但调用Spam3时不写ids,那么ids不会传入
        print("in metaclass Cached __call__()", args, *args, kwargs)
        if kwargs["ids"] in self.__cache:  # args是个turple(一个参数),若前面加*则是解包(多个参数),按组合查询是否在__cache中.
            print(list(self.__cache))
            return self.__cache[kwargs["ids"]]
        else:
            obj = super().__call__(*args, **kwargs)  # Spam3的初始化参数在__init__()每个都进行赋值.*args相当于传入多个参数.
            self.__cache[kwargs["ids"]] = obj
            return obj


class Spam3(metaclass=Cached):
    def __init__(self, name, age, ids=0) -> None:
        print("Creating Spam3")
        self.ids = ids
        self.name = name
        self.age = age

