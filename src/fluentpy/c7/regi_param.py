from functools import wraps


def register(active=False, r=set()):
    """ pycookbook C9.4 ,如果想不断增长,registry需要是global,定义在module级别.
        此外,使用一下这种方法,控制每个新的register执行时registry不会重新初始化. """
    # try:
    #     register.count += 1
    # except AttributeError:
    #     register.count = 0
    #     register.registry = set()
    try:
        register.registry.__str__()
    except AttributeError:
        register.registry = set()
    print(f"registry:{id(register.registry)} it's len->{len(register.registry)}")

    def decorate(func):
        """ decorate并没有执行func,只是把func添加进registry,带参数的装饰器2演示执行func
        此时需要再定义一层. """
        print(f"running register(active={active}) -> decorate({func})")
        if active:
            r.add(func)
            register.registry.add(func)
        else:
            r.discard(func)
        print(f"complete regi, registry:{id(register.registry)} it's len->{len(register.registry)}")
        print(f"r:{id(r)} it's len->{len(r)}")
        return func

    # 以下啰嗦,等同于 decorate.get_registry = lambda:registry
    # def get_registry():
    #     return registry

    # 把get_registry绑定给decorate函数的get_registry属性
    # 意味着decorate具备了get_registry函数的能力
    # decorate.get_registry = get_registry

    decorate.get_registry = lambda: register.registry
    return decorate


@register(active=False)
def f1():
    print("running f1()")


@register()
def f2():
    print("running f2()")


def f3():
    print("running f3()")


@register(active=True)
def f4():
    print("running f4()")


@register(active=True)
def f5():
    print("running f5()")

