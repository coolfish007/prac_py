from functools import wraps, partial
import logging


def attach_method_to_wrapper(wrapper_func, attach_method=None):
    if attach_method is None:
        print("attach_method is None. get attatch_wrapper...")
        return partial(attach_method_to_wrapper, wrapper_func)
    # print("func is not None, execute attach_wrapper with func")
    # 动态语言的强大之处,运行时给wrapper绑定一个方法
    # 上面return partial()这种用法会经常用,返回自己
    setattr(wrapper_func, attach_method.__name__, attach_method)
    return wrapper_func


def loggeds(func=None, *, level=logging.DEBUG, name=None, message=None):
    """ 关键是最后需要把func传入,但是由于要接收其他参数func是可选的.
        一开始,绑定非func的参数之后就返回.
        装饰器最终是要把被装饰的函数传入,会接着向下执行返回装饰器. """
    if func is None:
        print("Condition func=None, return func loggeds...")
        return partial(loggeds, level=level, name=name, message=message)
    print("Condition func not None, execute loggeds with func...")
    logname = name if name else func.__module__
    log = logging.getLogger(logname)
    logmsg = message if message else func.__name__

    @wraps(func)
    def wrapper(*args, **kwargs):
        log.log(level, logmsg)
        return func(*args, **kwargs)

    # 做法1:静态用法,或改为用函数写死.
    wrapper.logmsg = logmsg

    # 做法2:用函数代替
    def msg_it():
        return logmsg

    wrapper.msg_it = msg_it

    # 做法3:动态绑定get_msg到wrapper,set_msg也一样
    # 这样就不用手动把方法绑定到wrapper上了
    # 相当于attach_method_to_wrapper(wrapper)(get_msg)
    @attach_method_to_wrapper(wrapper)
    def get_msg():
        return logmsg

    @attach_method_to_wrapper(wrapper)
    def set_msg(new_msg):
        nonlocal logmsg
        logmsg = new_msg

    return wrapper
