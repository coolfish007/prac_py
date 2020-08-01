from functools import wraps
import inspect
from inspect import signature


def optional_debug(func):
    if "debug" in inspect.getargspec(func).args:
        raise TypeError("debug argument already defined")

    @wraps(func)
    def wrapper(*args, debug=True, **kwargs):
        if debug:
            print(f"Calling {func.__name__}")
        return func(*args, **kwargs)

    sig = inspect.signature(func)
    parms = list(sig.parameters.values())
    parms.append(inspect.Parameter("debug", inspect.Parameter.KEYWORD_ONLY, default=True))
    wrapper.__signature__ = sig.replace(parameters=parms)
    return wrapper
