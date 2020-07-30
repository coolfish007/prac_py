from functools import wraps
import logging


def logged(level, name=None, message=None):
    def decorate(func):
        logname = name if name else func.__module__
        log = logging.getLogger(logname)
        logmsg = message if message else func.__name__

        # 这个func与decorate(func)中的func保持一致.
        # @wraps(func)
        def wrapper(*args, **kwargs):
            log.log(level, logmsg)
            return func(*args, **kwargs)

        # 此写法等于@wraps(func),@wraps的调用结构
        # return wraps(func)(wrapper)
        f = wraps(func)
        # 返回functools.partial(update_wrapper,...)
        # update_wrapper是函数,并固定wrapped/assigned(默认值WRAPPER_ASSIGNMENTS)/updated(默认值WRAPPER_UPDATES)
        print(f"wraps(func)->{f}")
        # 相当与执行 update_wrapper(wrapper,wrapped,assigned,updated),后三个值已被固定;
        # 把把wrapped函数的属性拷贝到wrapper函数中.
        f = f(wrapper)
        # 以下两个都是wrapper,但属性值不一样.
        print(f"wrapper->{wrapper}")
        print(f"wraps(func)(wrapper)->{f}")
        return f

    return decorate


@logged(logging.DEBUG)
def add(x, y):
    return x + y


@logged(logging.CRITICAL, "example")
def spam():
    print("spam!")

