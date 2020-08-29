def log_getattri(cls):
    orig_getattri = cls.__getattribute__

    def new_getattri(self, name):
        print("getting attribute: ", name)
        return orig_getattri(self, name)

    cls.__getattribute__ = new_getattri
    return cls
