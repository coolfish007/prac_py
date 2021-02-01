#valid syntax => await is in async function
async def normal_func():
    await print("#")

#invalid syntax => await is not in async function
def invalid_normal_func():
    await print("#")

#invalid syntax => yield is in async function
async def invalid_normal_func2():
    yield "#"
