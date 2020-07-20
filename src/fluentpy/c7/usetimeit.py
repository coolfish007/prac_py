import time
import functools
from .timeit import clock


@clock
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
