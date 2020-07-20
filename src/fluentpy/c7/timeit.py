import time


def clock(func):
    def clocked(*args):
        t0 = time.perf_counter()
        # 会丢失**kwargs参数
        result = func(*args)
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_str = ", ".join(repr(arg) for arg in args)
        print(f"{elapsed:011.8f} {name}({arg_str}) --> {result}")
        return result

    return clocked

