from functools import wraps


def register(active=False):
    """ pycookbook C9.4 ,如果想不断增长,registry需要是global,定义在module级别 """
    registry = set()

    def decorate(func):
        """ decorate并没有执行func,只是把func添加进registry,带参数的装饰器2演示执行func
        此时需要再定义一层. """
        print(f"running register(active={active}) -> decorate({func})")
        if active:
            registry.add(func)
        else:
            registry.discard(func)
        print(f"complete regi, registry len->{len(registry)}")
        return func

    def get_registry():
        return registry

    decorate.get_registry = get_registry

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

