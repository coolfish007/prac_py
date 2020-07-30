# 装饰器返回原函数对象,可用于将C6中将策略进行注册.
registry = []


def register(func):
    print(f"run register({func})")
    registry.append(func)
    return func


@register
def f1():
    print("running f1()")


@register
def f2():
    print("running f2()")


def f3():
    print("running f3()")


""" if __name__ == "__main__":
    print("running main")
    print("registry ->", registry)
    f1()
    f2()
    f3() """
