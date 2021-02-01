#coroutine
from types import coroutine

@coroutine
def spam():
    result = yield 'somevalue'
    print("The result is", result)

f = spam()
print(">>>> send1")
print(f.send(None))
print()
print(">>>> send2")
print(f.send(None))
