import weakref


class Spam:
    _spam_cache = weakref.WeakValueDictionary()

    def __new__(cls, name):
        print("in __new__()")
        if name in cls._spam_cache:
            return cls._spam_cache[name]
        else:
            self = super().__new__(cls)
            cls._spam_cache[name] = self
            return self

    def __init__(self, name):
        print("in __init__()")
        self.name = name

