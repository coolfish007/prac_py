# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.4.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Practice of Python Elemnets

# %% [markdown]
# ## list

# %%
l = [1, 6, 7, 3, 8, 4, 2, 9, 5]
p = l[-1]
l[:-1]

# %%
l = [x for x in l[:-1] if x < p] + [p] + [x for x in l[:-1] if x > p]
l

# %%
a = 42
print(type(a))
print(id(a))
b = "guangzhou python "
print(b * 2)

# %%
a, b = b, a
print(a, b)

# %%
l = [1, 2, 3, 4, 5]
l_plus_2 = [i + 2 for i in l]
l_plus_2

# %% jupyter={"outputs_hidden": true}
import pandas as pd
import gzip

# %matplotlib inline

# %% jupyter={"outputs_hidden": true}
def parse(path):
    g = gzip.open(path, "r")
    for l in g:
        yield eval(l)


def load_dataset(path: str) -> pd.DataFrame:
    df = [d for d in parse(path)]
    return pd.DataFrame.from_dict(df)


# %%
print(7 / 4)
print(7 // 4)

# %% [markdown]
# ## 比较

# %%
x = 40
y = 42
z = 100
print(x < y <= z)

# %%
list1 = [1, 2, 3]
list2 = [1, 2, 3]
print(list1 is list2)
print(list1 == list2)
str1 = "abc"
str2 = "abc"
print(str2 is str1)
print(str2 == str1)

# %% [markdown]
# ## 切片
# 字符串本质上是一个List

# %%
a = "abcdefghijklmn"
print(a[::-1])
print(a[::2])
print(a[1:10:3])
print(a[:20])
print("-" * 20)
b = "hello world"
c = b[:]
print(id(b), id(c))
d = b
print(id(b), id(c), id(d))

# %%
a = [1, 2, 3, 4, 5]
print(a[:], a[::], a[1:5:2], a[2:5:4])
print(a[::-1], a[4::-1], a[4:2:-1], a[4:0:-1], a[4:-1:-1])

# %% [markdown]
# range 函数的使用，理解range返回的是一个迭代器，可以在上面使用切片。

# %%
for i in range(1, 3):
    print(i, end="")

print("\n")
print(type(range(3)))
for i in range(0, 100, 3):
    print(i, end=" ")
print([1, 2, 3, 4, 5, 6, 7, 8, 9, 10][0:3])
print(range(1, 6)[:2])  # 返回还是一个range
[
    [num for num in re] for re in [range(1, 101)[i : i + 3] for i in range(0, 100, 3)]
]  # 两个循环，一个是下标，一个是迭代


# %% [markdown]
# ## 格式化打印
#
# 1. 字符串的format方法：

# %%
pyStr1 = "string one"
pyStr2 = "string two"
print("Python's way one: {0} and {1}".format(pyStr1, pyStr2))
print("Python's way two: {s1} and {s2}".format(s1="China", s2="USA"))
print("Python's way three,like c. String %s and %s" % (pyStr1, pyStr2))

# %% [markdown]
# 类似于C的方法，用占位符。

# %% [markdown]
# 2. 字符串简单操作：
# split，strip，ltrip，rtrip，join

# %% [markdown] toc-hr-collapsed=true toc-nb-collapsed=true
# ## 高级特性

# %% [markdown]
# ### 列表生成式 List Comprehensions

# %%
list(range(1, 10))

# %%
[x * x for x in range(1, 10)]

# %%
[x * x for x in range(1, 10) if x % 2 == 0]

# %%
[m + n for m in "ABC" for n in "XYZ"]

# %%
import os

[d for d in os.listdir("..")]

# %% [markdown]
# 这个写法挺特别，一般条件判断不是写在后边么？

# %%
_list = [x if x % 2 == 0 else x * 2 for x in range(10)]
_list

# %%

# %%
d = {"x": "A", "y": "B", "z": "C"}
for k, v in d.items():
    print(k, " = ", v)

# %%
L = ["Hello", "1", "2", 183, "Python"]
[s.lower() for s in L if isinstance(s, str)]

# %%
a = [1, 2, 3]
b = [4, 5, 6]

product = [[x * y for x in a] for y in b]
for x in product:
    print(x)


# %% [markdown]
# ### 生成器和yield

# %%
def yield_test(n):
    for i in range(n):
        print("in yield_test,i=", i)
        # yield相当于return，完事了可以接着执行
        yield call(i)
        print("i=", i)
    # 做一些其它的事情
    print("do something.")
    print("end.")


def call(i):
    return i * 2


# 调用函数的时候并没有执行，yield_test只是个对象
print(yield_test(2))
# 使用for循环，才开始执行
for i in yield_test(2):
    print("out i=", i, ",")


# %% [markdown]
# #### 菲波齐纳数列
#
# * 使用yield，每次打印一个斐波那契数列的一个数字

# %%
def fib(max):
    n, a, b = 0, 0, 1
    while n < max:
        yield b
        a, b = b, a + b
        n = n + 1
    return "done"


for n in fib(5):
    print(n)


# %% [markdown]
# * 递归求斐波那契数列

# %%
def fib2(max):
    if max <= 1:
        return 1
    else:
        return fib2(max - 1) + fib2(max - 2)


for i in range(6):
    print(fib2(i))

# %% [markdown]
# * 杨辉三角形

# %%
l = [1, 2, 1]
print([l[i] + l[i + 1] for i in range(len(l) - 1)])


def triangles(max):
    l = [1]
    n = 0
    while n < max:
        yield l
        l = [1] + [l[i] + l[i + 1] for i in range(len(l) - 1)] + [1]
        n = n + 1
    return "done"


for n in triangles(5):
    print(n)

# %% [markdown]
# * 递归求和，分而治之。

# %%
l = [4, 5, 6]
# l[i]+l[i+1:]
i = 0


def sum1(l):
    if l == []:
        return 0
    return l[0] + sum1(l[1:])


print(sum1(l))


# %% [markdown] toc-hr-collapsed=true toc-nb-collapsed=true
# ## 函数参数

# %% [markdown] toc-hr-collapsed=true toc-nb-collapsed=true
# ### 关键字参数

# %%
def printscore(**kw):
    print(" " * 8 + "Name " + "Score")
    print("-" * 20)
    for k, v in kw.items():
        print("%12s %d" % (k, v))


data = {"lhc": 100, "lhc2": 90, "lhc3": 80}

printscore(**data)
print()
printscore(john=20, tom=55)


# %% [markdown]
# ### 命名关键字参数
# 命名关键字的函数，调用时必须传入参数规定的名字，这一点跟函数普通的调用不同。

# %%
def print_info(name, *, gender, city="Beijing", age):
    print("Personal Info")
    print("---------------")
    print("   Name: %s" % name)
    print(" Gender: %s" % gender)
    print("   City: %s" % city)
    print("    Age: %s" % age)
    print()


print_info("Bob", gender="male", age=20)
print_info("Lisa", gender="female", city="Shanghai", age=18)


# %% [markdown]
# ### 可变参数

# %%
def calc(*nums):
    sum = 0
    for i in nums:
        sum = sum + i * i
    return sum


calc(1, 2, 3)

# %%
# 来自于python cookbook 3rd Edition
line = "nobody:*:-2:-2:Unprivileged User:/var/empty:/usr/bin/false"
uname, *fields, homedir, sh = line.split(":")
print(uname)
print(fields, homedir)  # 不明白断开的位置。

record = ("Dave", "dave@example.com", "773-555-1212", "847-555-1212")
# 用星号代替的永远都是List类型
name, email, *phone_numbers = record
phone_numbers

# %%
t = ("AAA", 1.11)
result = ["something"]
result = result + list(t)
result = result + list(t)
print(result)
result.append(list(t))
print(result)

# %% [markdown]
# ## 函数式编程
# 把函数当做参数传入，这样的函数称为高阶函数，这样高度抽象的编程范式可以称之为函数式编程。

# %%
f = abs
f(-50)


# %% [markdown]
# ### map()函数
# 接收两个参数，一个是函数，一个是 Iterable，
# map 将传入的函数依次作用到序列的每个元素，并把结果作为新的 Iterator 返回。
# 做为传入参数的函数，需要return值。
#
# 字符串也是一个list。

# %%
def normalize(name):
    return name.capitalize()


L1 = ["adma", "LISA", "barT"]
L2 = list(map(normalize, L1))
print(L2)

# %% [markdown]
# ### reduce()函数
# 函数把一个函数作用在一个序列[x1, x2, x3, ...] 上，这个函数必须接收两个参数
# reduce 把结果继续和序列的下一个元 素做累积计算，其效果就是：

# %%
from functools import reduce


def prod(x, y):
    return x * y


reduce(prod, [3, 5, 7])

# %%
s = "101.256"
s = s.split(".")
list(map(int, s[0]))
print(list(map(int, s[1])))


def prod1(x, y):
    return x * 10 + y


def prod2(x, y):
    return x / 10 + y


a = reduce(prod1, list(map(int, s[0])))
b = reduce(prod2, list(map(int, s[1][::-1]))) / 10
a
b
a + b


# %% [markdown]
# ### filter()函数

# %%
def odd_iter():
    n = 1
    while True:
        n = n + 2
        yield n


for i in odd_iter():
    print(str(i) + ",", end="")
    if i > 100:
        break


# %% [markdown]
# filter()返回的是一个迭代器，必须用list转换,一旦使用list，就把数据都放到内存中去了。

# %%
def is_palindrome(n):
    s1 = str(n)
    return s1 == s1[::-1]


output = filter(is_palindrome, range(1, 1000))
print("1~500:", list(output))
if list(filter(is_palindrome, range(1, 200))) == [
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    11,
    22,
    33,
    44,
    55,
    66,
    77,
    88,
    99,
    101,
    111,
    121,
    131,
    141,
    151,
    161,
    171,
    181,
    191,
]:
    print("测试成功!")
else:
    print("测试失败!")


# %% [markdown]
# ### sorted函数

# %%
L = [("Bob", 75), ("Adam", 92), ("aart", 66), ("Lisa", 88)]


def by_name(t):
    print(t[0])
    s = t[0].lower()
    return s


L1 = sorted(L, key=by_name)
print(L1)

# %% [markdown]
# ### lambda 匿名函数

# %%
L = list(filter(lambda x: x % 2 == 0, range(1, 20)))
L


# %% [markdown]
# ### 装饰器

# %%
def log(func):
    def wrapper(*args, **kw):
        print("call %s():" % func.__name__, func)
        return func(*args, **kw)

    print("wrapper is {0}", wrapper)
    return wrapper


@log
def now():
    print("2015-3-25")


# 相当于执行了 now=log(now)
now()
print("now现在指向了wrapper，", now)
# 再次执行时，只执行了wrapper里边的语句。now的指向变了。
now()

# %% [markdown] toc-hr-collapsed=true toc-nb-collapsed=true
# ## 文件IO

# %% [markdown]
# 这个mode参数可以是
# * 'r' 只读模式（when the file will only be read）
# * 'w' 只写模式（与一个现存文件文件同名，则被清除）
# * 'a' 添加模式，即任意写入文件的数据都被自动添加到末尾
# * 'r+' 打开文件，可以读、写

# %%
import sys

f = open("./1.txt", "r")
f.read()
f.close()

with open("./1.txt", "r") as f:
    for line in f.readline():
        print(line, end=" ")


# %%
def findmax(l):
    max_num = l[0]
    max_index = 0
    for i in range(1, len(l) - 1):
        if max_num < l[i]:
            max_num = l[i]
            max_index = i
    return max_index


l = [5, 54, 98, 101, 3, 21, 44]
i = findmax(l)
print(l[i])

# %% [markdown]
# ## 文件与目录
# ### 使用内置pathlib

# %%
import pathlib
from IPython.display import display

display(pathlib.Path.cwd())
display(pathlib.Path("..").resolve())
display(pathlib.Path.cwd().parent / "src")
data_dir = pathlib.Path.cwd().parent.joinpath("data")
data_dir.parent

# %%
cwd_dir = pathlib.Path("..")
[d for d in cwd_dir.iterdir() if d.is_dir()]

# %%
cwd_dir = pathlib.Path(".")
display(cwd_dir)
display(cwd_dir.owner())
cwd_dir.joinpath("hello").mkdir(exist_ok=True)
cwd_dir.joinpath("hello").rmdir()

# %%
cwd_dir = pathlib.Path(".")
for py in cwd_dir.glob("*.py"):
    print(f"Exist python script:{py},type:{type(py)}")
# rglob遍历子目录
ipys = [str(ipy) for ipy in cwd_dir.rglob("*.ipynb")]
print(f"Exist ipy script:{';'.join(ipys)}")

# %% [markdown]
# ### 使用wcmatch
# #### wcmatch的pathlib
# %%
from wcmatch import pathlib

display(pathlib.Path.cwd())
pathlib.Path.cwd().joinpath("abc.java").touch(exist_ok=True)
display(pathlib.Path("..").resolve())
display(pathlib.Path.cwd().parent / "src")
data_dir = pathlib.Path.cwd().parent.joinpath("data")
display(pathlib.Path.cwd())

# %%
from wcmatch import pathlib

# What this means is when you are matching a path in the form some/path/name,
# the patterns name, path/name and some/path/name will all match.
display(pathlib.Path.cwd())
# 匹配路径,如果匹配当前路径的名称并向前,就像已经加了**一样,用match
display(pathlib.Path.cwd().match(["*_py/py*", "*-exercis"]))  # , flags=pathlib.GLOBSTAR)
display(pathlib.Path.cwd().match(["py*", "*-exercis"]))  # , flags=pathlib.GLOBSTAR)
# 这个为什么是true?没有globstar,不会匹配多个目录,按一层处理,
# 而prac_py/*是因为是当前目录的上一层?
display(pathlib.Path.cwd().match(["prac_py/*", "*-exercis"]))  # , flags=pathlib.GLOBSTAR)
ak = pathlib.Path.cwd() / "ak"
display(ak)
# ak目录的上一层不是prac_py,所以**没用,需加上globstar.
display(ak.match(["**/prac_py/**", "*-exercis"]))  # , flags=pathlib.GLOBSTAR)
# 而这个是false?加上globstar就能匹配.
display(
    pathlib.Path.cwd().match(["**/repo/**", "*-exercis"], flags=pathlib.GLOBSTAR)
)  # , flags=pathlib.GLOBSTAR)
# 写成**/repo/**不匹配,需要加globstar.用match,避免**开头.
display(pathlib.Path.cwd().match(["**/repo/**", "*-exercis"], flags=pathlib.GLOBSTAR))
# 如果匹配路径中的某一个目录,并且不知道层次,用globmatch安全一些.路径用**,名称匹配用*
display(pathlib.Path.cwd().globmatch(["**/rep*/**", "**/*-exerci"], flags=pathlib.GLOBSTAR))
# 必须加globstar
display(pathlib.Path.cwd().globmatch(["**/repo/**", "**/*-exerci"]))
display(pathlib.Path.cwd().globmatch(["**/py*", "**/*-exerci"], flags=pathlib.GLOBSTAR))
display(pathlib.Path.cwd().globmatch(["**/lhc/**", "**/*-exerci"], flags=pathlib.GLOBSTAR))
display(f'{pathlib.Path(".")},type:{type(pathlib.Path("."))}')
display(pathlib.Path(".").globmatch(["**/*po/**", "**/*-exerci"], flags=pathlib.GLOBSTAR))
# [m for m in pathlib.Path(".").glob(["*.java", "*.py"])]

# %%
from wcmatch import pathlib

# 匹配目录下的文件
p = pathlib.Path(".").glob(["*.py", "*.java"])
# result = list(p)
# display(result)
for f in p:
    print(f"Exist script:{f}:{f.resolve()},type:{type(f)}")

# %%
from wcmatch import pathlib

# 必须有*这种包含的模式
p = pathlib.Path(".").glob(["*", "!*.py"], flags=pathlib.NEGATE)
display(list(p))
p = pathlib.Path(".").glob(["*.py", "!py-*.py"], flags=pathlib.NEGATE)
display(list(p))
# 如果不用pattern list,那么需要标明SPLIT
p = pathlib.Path(".").glob("*|!*.py", flags=pathlib.NEGATE | pathlib.SPLIT)
display(list(p))
# NEGATEALL必须配合着NEGAT一起,否则无效
p = pathlib.Path(".").glob("!*.py", flags=pathlib.NEGATE | pathlib.NEGATEALL)
display(list(p))
p = pathlib.Path(".").glob(["*", "!*.py", "!*.java"], flags=pathlib.NEGATE)
list(p)
# result = glob.glob("!*.py", root_dir=".", flags=glob.NEGATEALL)
# display(result)

# %% [markdown]
# #### wcmatch 的 fnmatch
# %%
from wcmatch import fnmatch
from wcmatch import pathlib

p = pathlib.Path(".").glob(["*.py", "*.java", "a*"])
for f in p:
    if fnmatch.fnmatch(str(f), "!(*.go|*.c)", flags=fnmatch.EXTMATCH):
        print(f"no go or c: {f}")
pathlib
# %% [markdown]
# #### wcmatch 的 glob
# 以上和以下wcmatch.WcWatch()都是基于glob构造的

# %%
from wcmatch import glob

# 返回. 和 ..
display(glob.glob("ak/.*"))
# 只返回其下的所有目录
display(glob.glob("*/"))
# display(glob.glob("/**/lhc/dev/repo/*.", flags=glob.GLOBSTAR))
# **/匹配所有目录,下面返回上一层目录下的所有目录.
display(glob.glob("*/", root_dir=".."))
display(glob.glob("*"))

# 所有文件,包括隐藏文件,会包括.和..
display(glob.glob(".*"))
# 所有文件,不包含目录以及隐藏文件
display(glob.glob("*|!*/", flags=glob.NEGATE | glob.SPLIT))
display(glob.glob("[a-zA-Z0-9]*.*"))
display(glob.glob("[[:alnum:]]*.*"))
display(glob.glob("*", root_dir="ak/"))

# %%
from wcmatch import glob

display(glob.glob("[de]ef.java"))
# 以下不支持.
display(glob.glob("ef$.java"))
# 目录深度是第一层和第二层:find . -name '[a-g]*.java' -maxdepth 2
display(glob.glob(["[a-g]*.java", "*/[a-g]*.java"]))
# 目录深度是第3层
display(glob.glob(["*/*/[a-g]*.java"]))
# 包含子目录,**如果代表多层目录,需要加globstar
display(glob.glob("**/[a-g]*.java", flags=glob.GLOBSTAR))


# %% [markdown]
# #### wcmatch
# wcmatch 基于glob和fnmatch构建更容易使用的API
# %%
from wcmatch import wcmatch

matchit = wcmatch.WcMatch(".", "!*.py|!*.ipynb", flags=wcmatch.HD | wcmatch.RV).match()
display(type(matchit))
for m in matchit:
    display(f"element type:${type(m)}")
    display(f"Absolute path of java file:{pathlib.Path(m).resolve()}")
display(f"match files: {','.join(matchit)}")

# %%
matchit = wcmatch.WcMatch(".", "test*", flags=wcmatch.HD | wcmatch.RV).match()
# matchit = wcmatch.WcMatch(".", r"\w{4}", flags=wcmatch.HD | wcmatch.RV | wcmatch.RAWCHARS).match()
matchit
# %%
# 注意template的用法,也用wcmatch实现.
def unique_path(directory, name_pattern):
    counter = 0
    while True:
        counter += 1
        path = directory / name_pattern.format(counter)
        if not path.exists():
            return path


path = unique_path(pathlib.Path.cwd(), "test{:03d}.txt")

# %%
from string import Template

name = "coolfish"
Template("hello, $name!").substitute(name=name)


# %%

