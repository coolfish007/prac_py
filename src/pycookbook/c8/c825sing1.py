import weakref


class CachedSpamManager:
    def __init__(self) -> None:
        self._cache = weakref.WeakValueDictionary()

    def get_spam(self, name):
        if name not in self._cache:
            tmp = Spam2._new(name)
            self._cache[name] = tmp
        else:
            tmp = self._cache[name]
        return tmp

    def clear(self):
        self._cache.clear()


class Spam2:
    manager = CachedSpamManager()

    def __init__(self, *args, **kwargs):
        raise RuntimeError("Cannot instantiate directly")

    @classmethod
    def _new(cls, name):
        self = cls.__new__(cls)
        self.name = name
        return self

    @staticmethod
    def get_instance(name):
        Spam2.manager.get_spam(name)
