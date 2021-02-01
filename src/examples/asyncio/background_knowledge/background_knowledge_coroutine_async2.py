from types import coroutine

@coroutine
def spam():
    result = yield 'somevalue'
    print("The result is", result)

async def foo():
    print("Start foo()")
    await spam()
    print("End foo()")

async def bar():
    print("Start bar()")
    await foo()
    print("End bar()")

f = bar()
print(">>>> send1")
print(f.send(None))
print()
print(">>>> send2")
print(f.send(None))
