from types import coroutine

@coroutine
def spam():
    result = yield 'somevalue'
    print("The result is", result)

async def foo():
    print("Start foo()")
    await spam()
    print("End foo()")

f = foo()
print(">>>> send1")
print(f.send(None))
print()
print(">>>>  send2")
print(f.send(None))
