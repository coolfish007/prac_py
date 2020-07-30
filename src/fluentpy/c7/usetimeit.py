import time
import functools
from .timeit import clock


@clock
# 只有func做参数,一致性的体现,不用带();
# 此时带上()需要填写func参数.
def snooze(seconds):
    time.sleep(seconds)


@clock
def factorial(n):
    return 1 if n < 2 else n * factorial(n - 1)


@clock
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 2) + fibonacci(n - 1)


@functools.lru_cache()
@clock
def fibonacci_cache(n):
    if n < 2:
        return n
    return fibonacci_cache(n - 2) + fibonacci_cache(n - 1)
