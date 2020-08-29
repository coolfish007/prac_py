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
#     display_name: 'Python 3.8.2 64-bit (''data'': venv)'
#     name: python38264bitdatavenv86c8e9e79e034983bf9e66a89847a1a4
# ---

# %% [markdown]
# 动态在pathlib中插入src

# %% tags=[]
import sys
import os
from IPython.display import display
from wcmatch import pathlib

display(sys.executable)
src_p = pathlib.Path("..") / "src"
if src_p.exists() and src_p.is_dir():
    print(f'insert {src_p.resolve()} in PythonPath')
    sys.path.insert(0, os.fspath(src_p.resolve()))

# %% [markdown]
# # 1 context manager

# %% [markdown]
# # 2 Function

# %%
fruits = ['strawberry', 'fig', 'apple', 'cherry', 'raspberry', 'banana']
sorted(fruits, key=len)


# %%
def reverse(word):
    return word[::-1]
reverse('hello')
sorted(fruits,key=reverse)


# %% [markdown]
# ## 2.1 map()
# 特别是一个序列做map,直接用生成器表达式替换.

# %%
def factorial(n):
    return 1 if n<2 else n*factorial(n-1)

display(list(map(factorial, range(6))))
[factorial(n) for n in range(6) if n%2]

# %% [markdown]
# ## 2.2 函数内置属性

# %% tags=[]
for n in dir(factorial):
    print(n,end='/')
print('\n')
fac = factorial
print(fac.__hash__())


# %% [markdown]
# ## 2.3 函数的参数
# flutpy C5.7的拆解
# ### 仅限关键字键值对的函数

# %%
def f(a,*,b=1):
    return a,b
f(1,b=9)

# %%
fac = factorial
display(f.__code__) # 属性非方法
display(f.__defaults__) # 为什么是None,仅限关键字参数?
display(fac.__defaults__)
f.__kwdefaults__

# %% tags=[]
from inspect import signature
sig = signature(f)
display(str(sig))
for name,p in sig.parameters.items():
     print(f'{name}, default value:{p.default}, kind:{p.kind}')

# %%
r = f(a=0,b=8)
r[0]

# %% [markdown]
# ### star assignment,Py 3.5+
# PEP 448,Additional Unpacking Generalizations / PEP 3132 -- Extended iterable unpacking

# %% tags=[]
a=1,2
print(type(a),a)
*a,=[[1,2,3],[4,5,6]]
print(type(a),a)


# %% tags=[]
# Whilst *elements, = iterable causes elements to be a list, elements = *iterable, causes elements to be a tuple.
# *b, 类似于函数定义 fun(*arg,**kwargs)), * in left side means catch everything that isn't assigned to a name and assign it to the starred expression.
*b,=3,4,5
print(type(b),b) 
for i in b:
    print(type(i),end='')
print('\n')
*b,=(6,7,8) #拿出tuple元素往*b中填,形成list
print(type(b),b)
for i in b:
    print(type(i),end='')
print('\n')
*b,c,d=3,4,5
print(type(b),b)

iterable = [1,2,3,4]
b = *iterable, #可看做 b=1,2,3,4,It expands the contents of the iterable it is attached to.
print(type(b),b)
b=[*iterable]
print(type(b),b)


# %% [markdown]
# ### *可变参数

# %% tags=[]
def fun(a,*num):
    print(type(num),num)
fun(1) # 变长参数会转换成turple,这和*iterable是一直的,都是turple
fun(1,2,3,4) 
fun([1,2,3,4])

iterable = [1,2,3,4]
fun(*iterable)
iterable=([1,2],[3,4],5)
fun(*iterable)
iterable = {1:1,2:2,3:3,4:4} #*只解包dict的key
fun(*iterable)


# %% [markdown]
# ### ***关键字参数

# %% tags=[]
def fun(a,**kw):
    print(kw)
fun(1,name='lhc',age='30')
iterable = {'one':1,'two':2,'three':3,'four':4} 
fun(1,**iterable)
iterable = {1:1,2:2,3:3,4:4} #fun() keywords must be strings,即变量名必须是strings
fun(1,**iterable)


# %% [markdown]
# ### 可变参数*之前的参数不能指定参数名

# %% tags=[]
def fun(a,*num):
    print(a,num)
fun(1,2,3)
fun(1,num=2) # TypeError: fun() got an unexpected keyword argument 'num'

# %%
fun(a=1,2,3) #SyntaxError: positional argument follows keyword argument


# %% [markdown]
# ### 可变参数*之后的参数必须指定参数名

# %% tags=[]
def fun(a,*b,c=None):
    print(a,b,c)
fun(1,2,3,4) # 若c没有默认值c=None:TypeError: fun() missing 1 required keyword-only argument: 'c'
fun(1,2,3,c=1)


# %% [markdown]
# ### 关键字参数只能作为最后一个参数
# 关键字前面的参数按照位置赋值还是名称赋值都可以.  
# **顺序：位置参数（必选参数），默认参数，单星号参数或星号分隔符，关键字参数，双星号参数；**  
# 默认参数和关键字参数很像,不要搞混,默认参数在加载时即赋值.

# %% tags=[]
def fun(a,*b,c=None,**d):
    print(a,b,c,d)
fun(1,2,3,4,m=5,n=6)
fun(1)
fun(1,2)
fun(1,2,q=0)


# %% [markdown]
# ### 解包作为参数传入函数

# %% tags=[]
def fun(a,b):
    print(a,b)
iterable = (1,2)
fun(*iterable)
iterable = [1,2,3,4]
fun(*iterable) # TypeError: fun() takes 2 positional arguments but 4 were given

# %% tags=[]
person1 = {'name':'lhc','age':30}
print("{name}'s age is {age}".format(**person1))


# %% [markdown]
#

# %% [markdown]
# ## 2.4 函数体也有属性

# %% tags=[]
def addIt(x,y):
    try:
        addIt.counter +=1
    except AttributeError:
        addIt.counter = 0
    print(f'execute {addIt.counter}')
    return x+y
addIt.a = 0
f = addIt
display(f(1,2))
print(f.a,f.counter)
addIt.a+=2
f = addIt
display(f(3,4))
print(f.a,f.counter)
addIt.__dict__

# %% [markdown]
# ## 2.5支持函数式编程的包
# 高阶函数演示.

# %%
from functools import reduce
from operator import mul, xor

def fact_re(n):
    """ reduce 结合 mul 计算阶乘 """
    return reduce(mul,range(1,n+1))

fact_re(5)

# %% [markdown]
# ### itemgetter()

# %% tags=[]
from operator import itemgetter
metro_data = [
    ('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),
    ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
    ('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
    ('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
    ('Sao Paulo', 'BR', 19.649, (-23.547778, -46.635833)),
]
cc_name = itemgetter(1,0)
for c in metro_data:
     print(cc_name(c))

itemgetter(3)(metro_data[3])

# %% [markdown]
# ### attrgetter() and namedtuple()

# %%
from operator import attrgetter
from collections import namedtuple

# 参数1是namedtuple的值
LatLong = namedtuple('LL','lat long')
Metro = namedtuple('Metro','name cc pop corrd')
# name,cc,pop,(lat,long) 对元组进行拆包,并赋予名称
# 之后给到namedtuple:Metro
metro_area = [Metro(name,cc,pop,LatLong(lat,long)) for name,cc,pop,(lat,long) in metro_data]

attrgetter('name','corrd.lat','corrd.long')(metro_area[2])

# %% [markdown]
# ### functools.partial

# %%
from operator import mul
from functools import partial

triple = partial(mul,3)
display(triple(7))
display(list(map(triple,range(1,11))))

# %% [markdown]
# ### function 实现 策略模式

# %% tags=[]
from fluentpy.c6.order import Customer
from fluentpy.c6.order import LineItem
from fluentpy.c6.order import Order
from fluentpy.c6.order import fidelity_promo

lhc = Customer('LHC48052', 999)
cart = [LineItem('banana',4,0.5),LineItem('apple',3,0.4)]
display(Order(lhc,cart,fidelity_promo))

cart = [LineItem('orange',5,0.7)]
display(Order(lhc,cart,fidelity_promo))

cart = 'abc'
for i in cart:
    print(type(i))
    print(i)
cart = list(list(cart))
for i in cart:
    print(type(i))
    print(i)

# %% [markdown]
# # 3 Iterator and Generator
# From Fluent Python Chapter 14.

# %% [markdown]
# ## Iterable 和 Iterator

# %% [markdown]
#

# %% tags=[]
from fluentpy.c14.sentence import Sentence1

s = Sentence1("Crazy world, extraordinary world.")
display(s)
i = iter(s)
for word in i:
    print(word)

for word in s:
    print(word)

# i 中已无可迭代的内容.
next(i)

# %% tags=[]
from fluentpy.c14.sentence import Sentence2

s = Sentence2("Crazy world, extraordinary world.")
for word in s:
    print(word)

# iter()每次构造新的迭代器
display(next(iter(s)))
display(next(iter(s)))

# 新的迭代器,重新开始
# while 不会捕捉stopiteration异常
i = iter(s)
while(True):
    display(next(i))



# %% [markdown]
# ## 迭代器中使用生成器函数 yield

# %% tags=[]
from fluentpy.c14.sentence import Sentence3

s = Sentence3("Sentence3, Crazy world, extraordinary world.")
for word in s:
    print(word)

next(iter(s))

# %% tags=[]
from fluentpy.c14.sentence import Sentence4

s = Sentence4("Sentence 4, Crazy world, extraordinary world.")
for word in s:
    print(word)


# %% [markdown]
# ## 生成器函数:yield from(广度和深度搜索)

# %% tags=[]
from pycookbook.c4.node44 import Node

root = Node(0)
c1 = Node(1)
c2 = Node(2)
c3 = Node(3)

root.add_child(c1)
root.add_child(c2)
root.add_child(c3)

c1.add_child(Node(11))
c1.add_child(Node(12))
c2.add_child(Node(21))
c3.add_child(Node(31))

for ch in root.depth_first():
    print(f'out print:{ch}')

print('======================')
for ch in root.depth_first_yield_from():
    print(f'out print:{ch}')

print('======================')
isRoot = True
for ch in root.width_first(isRoot):
    print(f'out print:{ch}')
    isRoot = False

# %% [markdown]
# # 4. Decroator

# %% [markdown]
# ## 4.1 装饰器加载即运行
# 函数的默认参数也是这个在装载时运行.

# %% tags=[]
import fluentpy.c7.regi as re



# %% tags=[]
# 导入后registry即有值
display(re.registry)
# 装饰器返回的还是原函数,所以f1的元数据保持不变.
display(re.f1.__name__)
re.f1()

# %%
import fluentpy.c7.average as av

# make_sum_average()运行后,生产出average
mav = av.make_sum_average()
display(mav(10))
display(mav(15))
mav.__code__.co_varnames

# %%
mav.__code__.co_freevars

# %%
# __closure__中保存着闭包的元素,本例中是series,cell_contents是series的值.
mav.__closure__[0].cell_contents

# %%
mav = av.make_average()
mav(10)
mav(12)


# %%
def x1():
    count += 1
    return count
x1()

# %% [markdown]
# ## 简单装饰器 timeit

# %% tags=[]
import fluentpy.c7.usetimeit as ut

print('*'*20,'Calling snooze(0.5)')
ut.snooze(0.5)
print('*'*20,'Calling factorial(6),6!=')
ut.factorial(6)
# 装饰器没有使用@wraps(),函数原来的信息丢失.
print(f'After decroator,factorial --> {ut.factorial.__name__}')

# %% tags=[]
import fluentpy.c7.usetimeit as ut

ut.fibonacci(5)

# %% tags=[]
import fluentpy.c7.usetimeit as ut

ut.fibonacci_cache(10)

# %% [markdown]
# ## 带参数的装饰器1
# fluentp C7-22.  
# 注意闭包的自由变量registry作用域.

# %% tags=[]
import fluentpy.c7.regi_param as regi_p

# 加载即运行,但装饰器每次一个新的register,导致registry没有累加
# 如果需要不断累加,像fluentpy C7.22中一样,把registry定义在module级别
# 这个主要想看下如何获取闭包的变量,如pycookbook C7.12

# %% tags=[]
f = regi_p.register
display(f)
# 手动注册,一直使用装饰器的引用
deco = f(active=True)
display(deco)
f_run = deco(regi_p.f1)
display(f_run)
# run f1()
f_run()
display(len(deco.get_registry()))
f_run = deco(regi_p.f3)
display(len(deco.get_registry()))
# run f3()
f_run()

# %% tags=[]
g = regi_p.register
deco = g(active=True)
f_run= deco(regi_p.f3)
f_run()

# %% [markdown]
# ## 带参数的装饰器2
# pycookbook C9.2和C9.4

# %% tags=[]
from pycookbook.c9.logged import *
import logging

logging.basicConfig(level=logging.DEBUG)
x = add
display(x)
display(x.__wrapped__)
display(x(2,3))
x(4,5)

# %% [markdown]
# 解构logged这个装饰器的运行机制

# %% tags=[]
from pycookbook.c9.logged import *
import logging

logging.basicConfig(level=logging.DEBUG)

def addIt(x,y):
    return x+y

logged(logging.CRITICAL)(addIt)(2,3)

f = logged(logging.CRITICAL)
display(f)
f = f(addIt)
# 由于@wraps的存在,这里保留了addIt的元信息.
# 否则返回: <function pycookbook.c9.logged.logged.<locals>.decorate.<locals>.wrapper(*args, **kwargs)>
# 如果返回了被decorate的func,就可以用实际参数进行调用了.
display(f)
f(3,4)

# %% [markdown]
# ## 带参数的装饰器3
# 参数可选:pycb C9.6

# %% tags=[]
from pycookbook.c9.loggeds import *
import logging

logging.basicConfig(level=logging.WARNING)
logging.debug('hi')

@loggeds
def addIt(x,y):
    return x+y



# %% tags=[]
display(addIt(2,3))
# log在函数定义时先执行了,等待addParam(3,3)的时候再执行.
print('*'*10)

@loggeds(level=logging.CRITICAL,message='addParam test',name='param example')
def addParam(x,y):
    return x+y

# 以下访问闭包属性
f = addParam
display(f.logmsg)
display(f(3,3))
f.set_msg('new_msg')
display('静态用法:',f.logmsg)
display('用函数:',f.msg_it())
display('动态用法:',f.get_msg())
display(f(4,4))

# %%
from pycookbook.c9.loggeds import *
import logging


# %% [markdown]
# loggeds运行时机和装饰器机制有关.见装饰器2的结构部分  
# 相当于loggeds(addIt),运行loggeds一次,func is not None

# %% tags=[]
@loggeds
def addIt(x,y):
    return x+y


# %% tags=[]
addIt(3,4)


# %% [markdown]
# 相当于loggeds(level=...)(addParam)  
# 第一次运行func is None,返回partial(loggeds,...)即还是loggeds,再次运行时func is not None

# %% tags=[]

@loggeds(level=logging.CRITICAL,message='addParam test',name='param example')
def addParam(x,y):
    return x+y


# %% [markdown]
# ## 将装饰器定义为类pycb C9.9

# %% [markdown]
# ### 类装饰器作用在方法上,起调__call__()

# %% tags=[]
from pycookbook.c9.profiled import Profiled

@Profiled
def add(x,y):
    return x+y


# %% tags=[]
add(3,4)

# %% [markdown]
# 解构装饰器,wraps的解构在profiled中.

# %% tags=[]
from pycookbook.c9.profiled import Profiled

def addIt(x,y):
    return x+y

p = Profiled(addIt)
print(f'***p:{p},p.__wrapped__:{p.__wrapped__}')
# p有__call__()函数,可调用,addIt(3,4)等同于p(3,4)
p(3,4)

# %% [markdown]
# ### TODO:将装饰器作用在类方法上
# 关联至5.@property 延迟计算.

# %% [markdown]
# ## 使用装饰器动态添加函数的参数 pycb C9.11

# %%
from pycookbook.c9.option_debug import *

@optional_debug
def add(x,y):
    return x+y


# %% tags=[]
display(add(2,3))

# %%
import inspect
display(inspect.signature(add))

# %% [markdown]
# ## 使用装饰器扩展类的功能pycb C9.12
# 装饰器作用在类之上.
# %% 
from pycookbook.c9.c912 import *

@log_getattri
class A:
    def __init__(self,x):
        self.x = x
    def spam(self):
        pass
    def __getattr__(self,name):
        return 'default'

a = A(40)
display(a.x)
display(a.y) #虽然重写了__getattribute__(),会捕捉attributeerror,不存在的属性会自动调用__getattr__()
# %% [markdown]
# # 5. Object Oriented

# %% [markdown]
# ## 函数参数是默认参数时
# HauntedBus隐藏的bug.

# %%
from fluentpy.c8.HauntedBus import HauntedBus

# 初始化有参数时无任何问题
bus1 = HauntedBus(['lhc'])
display(bus1.passengers)
bus1.pick('gxt')
bus1.drop('lhc')
display(bus1.passengers)


# %%
bus2 = HauntedBus()
bus2.pick('haunt')
display(bus2.passengers)

# 函数默认值在定义函数时计算,即在module加载时进行
bus3 = HauntedBus()
display(bus3.passengers)

# %% [markdown]
# ## SchoolBus 
# 正确的做法.

# %%
from fluentpy.c8.SchoolBus import SchoolBus

bus1 = SchoolBus()
bus1.pick('lhc')
display(bus1.passengers)

bus2 = SchoolBus()
bus2.pick('gcq')
display(bus2.passengers)

# %% [markdown]
# ## 属性及属性覆盖
# 每次属性查找，这个协议的方法实际上是由对象的特殊方法__getattribute__()调用。每次通过点号（ins.attribute）或者 
# getattr(ins, ‘attribute’)函数调用都会隐式的调用__getattribute__()，它的属性查找的顺序如下：
# 1. 若判断是描述器优先于实例变量
# 2. 查看该属性是否能在实例对象的dict中找到
# 3. 查看该属性是否为实例的类对象的非数据描述符(只实现了__get__(),可以理解成描述器退化成类的属性)
# 4. __getattri__()方法
# 关联描述器 Stock1 例子

# %% tags=[]
from fluentpy.c8.simple_bird import *Chicken, Chicken, Chicken, Chicken, Bird, Bird, Chicken, Chicken, Chicken, Bird, Chicken,  

summer = Chicken(2)
print('=====>summer')
print(summer.__dict__)
print(vars(summer)) #vars()返回__dict__属性
print(summer.fly)
print('=====>Chicken')
print(Chicken.__dict__)
print(vars(Chicken))
print('=====>Bird')
print(Bird.__dict__)
print(vars(Bird))

# %% tags=[]
print(summer.age,summer.fly)

# %%
summer.fly=True
display(summer.fly)  # 对象的属性赋值时,只会查找本对象的__dict__,若无此属性,自动添加.
display(summer.__dict__)
display(Chicken.__dict__)

# %% [markdown]
# 类的方法和函数的区别

# %% tags=[]
from fluentpy.c8.simple_bird import *
from inspect import signature

def outer_test(a):
    print('out of class')

ck = Chicken(2)
print(dir(ck.chirp))

# %% tags=[]
display(type(ck.chirp)) # chirp是method,又分为bound和unboud,属性方法;会隐含自动传入self
print(ck.chirp.__code__.co_varnames)
# TODO:signature(ck.chirp)会出错
for name,value in signature(ck.chirp.__call__).parameters.items():
    print(name,value)
ck.outer_test = outer_test
display(type(ck.outer_test)) #不会自动传入self
print(ck.outer_test.__code__.co_varnames)
print(signature(ck.outer_test))

# %% [markdown]
# ## super()的用法/解构--关联描述器
# super在不同参数下可以代表unbound、bound到对象、bound到类型，这点在docstring当中其实写的比较清楚了，
# Python3省略所有参数时候相当于super(self, class)，是bound到对象。而super(class, class)自然是绑定到了父类。
# **实质上是对描述器的理解加深,一个描述器,通过__get__()的访问,可以将描述器放置到某实例,即绑定.**
# %%
from fluentpy.c8.simple_bird import *

ck = Chicken(2)
display(Chicken.__mro__)
display(Chicken.__dict__)
display(Bird.__dict__)

# o = super()
# print(o)
# print(o.chirp)
o = super(Chicken, ck)  # ==类内部的super()的用法,mro链的内容由ck确定并绑定在ck上的Bird(Chicken的下一跳)的chirp方法.
print(o)
print(isinstance(o,super)) 
chirp1 = getattr(o,'chirp')
display(chirp1) # 已绑定至ck实例
print(o.chirp)
print(o.chirp())
print(o.funcname)
o = super(Chicken, Chicken)  # 同上注释,bound super object; requires issubclass(type2, type)
print(o)
chirp3=getattr(o,'chirp') # 未绑定至实例,为function
chirp4=o.chirp.__get__(None,Chicken) # 未绑定至实例,返回function本身
display(chirp3 is chirp4) #同一id
chirp2 = getattr(o,'chirp').__get__(ck) # function也是描述器,绑定至ck,为bound method
display(chirp2) 
display(chirp1==chirp2)
display(chirp1 is chirp2)
print(o.chirp)
print(o.chirp(ck))
print(o.funcname())  # funcname()绑定在Chicken上,这里默认传入的cls 是 Chicken
print("=" * 5, ">no second param.")
o = super(Chicken)  # unbound super object
print(hasattr(o, "chirp"))
b1 = o.__get__(ck,type(ck)) #o.__get__(ck,type(ck)),可以把o当做Chicken中的描述器,使用ck访问,bound super object
b2 = o.__get__(ck)
b3 = o.__get__(None,type(ck))
print(b1)
print(b2)
print(b1==b2)
print(b3) # 返回装饰器o本身,b3 is o
print(o is b3)
print(b2.__thisclass__) # Chicken
print(b2.__self__) #绑定至ck为ck这个实例,绑定至Chicken为Chicken这个类
print(b2.__self_class__)
print(isinstance(b1,super))
print(b1.chirp) # dispatch to the method of Bird.chirp
# print(type(o).__dict__) #在类上访问__dict__才能看到super(Chicken)里的内容.
print(b1.feather) # 如果访问fly出错,因为Bird没有fly的属性.
b1 = o.__get__(Chicken) 
b2 = o.__get__(Chicken,type(Chicken))
print(b1)
print(b2)
print(b1 == b2)
print(b1.chirp)
print(b1.chirp.__get__(ck)) # 将function chirp绑定至实例ck
print(b2.__thisclass__) # Chicken
print(b2.__self__) #绑定至ck为ck这个实例,绑定至Chicken为Chicken这个类
print(b2.__self_class__)
o = super(Bird)
print(hasattr(o, "chirp"))
# %% [markdown]
# ## Vector2d_v0: fulentpy C9.1
# 实现默认方法,不是每个类都需要这么实现,如果要借助内置方法如abs(),repr(),str()即可实现其方法,__iter__()使对象内容可迭代,即可用在类似于tuple()和list()之中.

# %%
import operator as op
from fluentpy.c9.vector2d_v0 import Vector2d

v = Vector2d(3,4)
display(abs(v))
display(op.eq(v,(3,4)))
display("{}({!r},{!r})".format(*[1,2]))

# %%
display(list(v))
len(list(v))

# %% tags=[]
v = Vector2d(3,4)
# 调用vector2d 自定义的__bytes__()
b = bytes(v)
display(b)

display(chr(b[0]))
display(b[1:])
v1 = Vector2d.frombytes(b)
display(v1)
display(v == v1)

# %% [markdown]
# ## 类属性的使用

# %% [markdown]
# ## Py的特性:@property

# %% [markdown]
# ### @property的基本使用
# 对属性first_name的访问均会通过getter和setter进行.

# %% tags=[]
from pycookbook.c8.person import *

p = Person('coolfish')
display(p.first_name)
p.first_name='coolfish007'
display(p.first_name)

# %% [markdown]
# 直接给内部属性赋值,绕过setter

# %%
p._first_name = 42
display(p.first_name)

# %% tags=[]
from pycookbook.c8.person import *

p = Person(42) #TypeError: Expected a string

# %% [markdown]
# ### 特性是类属性
# (*)特性被类直接访问赋值后,就地销毁.

# %% tags=[]
from pycookbook.c8.person import *

print(vars(Person))
print(dir(Person.first_name))
print(Person.first_name)
#Person.first_name='coolfish008' #赋值类属性
p = Person('coolfish') #赋值实例属性
print(Person.first_name)
print(vars(p))
print('Person.first_name.fget(p):')
print(Person.first_name.fget(p)) # 重复运行时,Person.first_name已变为str
print('p.first_name:',p.first_name)
Person.first_name='class name' # 覆盖特性,特性first_name被销毁,不再通过getter取值,setter赋值
print(Person.first_name)
print(vars(p))
print(p.first_name)
print(p._first_name)

# %% [markdown]
# ### 使用特性延迟计算并缓存结果

# %% tags=[]
from pycookbook.c8.c810lazy2 import *

c1 = Circle(2)

print(c1.area)

# %% [markdown]
# ### (*)lazy2 @property 解构

# %% tags=[]
from pycookbook.c8.c810lazy2 import *

c2 = Circle(3)
# 注意这个地方,需写成 类.method的方式,这样是一个function
# 这样调用时需显式的写成 method(self),手动传入self
# 否则若写成对象.method的方式如c2.perimeter,在lazy()中调用func(self),会自动传入self
# 这样,位置参数的数量就不一致了.
wrapped = Circle.perimeter
f = lazyproperty(wrapped)
print(dir(f))
print(f)
print(f.fget)
print(dir(f.fget))
print(f.fget(c2)) # property 绑定至c2

# %% [markdown]
# 特性是类属性,将特性f设置为Circle的类属性.  
# 之后可以直接在对象上访问属性perimeter.  
# 至此,解构彻底完成.

# %% tags=[]
setattr(Circle,'perimeter',f)  # fltpy P509,除了直接给__dict__的赋值,这些方法都会调用处理特性的特殊方法.
c3=Circle(4)
print(c3.perimeter)
print('cached perimeter')
print(c3.perimeter)

# %% tags=[]
from pycookbook.c8.c810lazy2 import *

c2 = Circle(3)
c2.perimeter

# %% [markdown]
# ## Py的描述器
# 类的实例类型;类的type()是type类型.

# %%
from pycookbook.c8.c813checkattri import *

name = SizedString('name',size=8)
display(type(name))
display(isinstance(name,Descriptor))
display(isinstance(name,Typed))
display(isinstance(name,String))
display(isinstance(name,MaxSized))

# %%
from pycookbook.c8.c813checkattri import *

ui = UnsignedInteger() # () 代表已构造类的实例
display(type(ui))
display(isinstance(ui,Descriptor))

ui = UnsignedInteger
display(type(ui))
display(isinstance(ui,Descriptor))
# 使用参数名称,用ui构造一个UnsignedInteger对象实例
display(isinstance(ui('shares'),Descriptor))
# 显示UnsignedInteger 的__set__来自于哪里
display(ui.__mro__)
display(ui.__set__)
# 显示__dict__
ui('share').__dict__

# %% [markdown]
# ### 多重继承

# %% [markdown]
# MRO 方法执行顺序

# %% tags=[]
import logging
from pycookbook.c8.c813checkattri import *

logging.basicConfig(level=logging.DEBUG)  # 之后再设置level,需要重启jupyter
logging.info('hi')
display(SizedString.__mro__)
name = SizedString('name',size=8)
print(dir(name))
name.__set__(name,6)  #按照__mro__的顺序,同一方法,进入typed,进入maxsized,进入descriptor执行,执行maxsized剩余的,执行typed剩余的.

# %% [markdown]
# ### 描述器的使用
# 描述器做为类属性

# %% tags=[]
import logging
from pycookbook.c8.c813checkattri import *

logging.basicConfig(level=logging.WARN)

class Stock1:
    name = SizedString('name',size=8)
    shares = UnsignedInteger('shares')
    price = UnsignedFloat('price')


    def __init__(self,name,shares,price):
        self.name = name #描述器和实例属性同名,描述器覆盖实例属性.
        self.shares = shares
        self.price = price

    def __getattr__(self,name):
        print(self,name)
        return 'default'

display(type(Stock1)) #type
display(isinstance(Stock1,type))

# %% [markdown]
# 关联类的属性和属性覆盖(调用顺序)
# %%
stock = Stock1('hello',5,3.0)
# display(Stock1.name.__get__(None,Stock1)) #描述器无__get__()方法,直接访问__dict__的内容.
display(stock.haha) # 无haha属性,调用__getattr__()
stock.name='hello2'
display(stock.__dict__['name'],stock.name,Stock1.name)
Stock1.name='haha3'  # 销毁了描述器,变成普通的str.
display(stock.name,Stock1.name)
# %% tags=[]
stock = Stock1('hello',5,3.0)
stock.name = 'hello1'
display(stock.name)
stock.price='hellohello' #error:size must be < 8

# %% [markdown]
# ### 描述器实现及使用:混入+装饰器的方式
# 使用装饰器check_attri+混入的方式做为类变量的检查器

# %% tags=[]
import logging
from pycookbook.c8.c813checkattri import *

logging.basicConfig(level=logging.INFO)

@check_attri(name=SizedString(size=8),shares=UnsignedInteger,price=UnsignedFloat)
class Stock2:
    def __init__(self,name,shares,price):
        self.name = name
        self.shares = shares
        self.price = price

s2 = Stock2('hello',5,3.0)
display(s2.name)

# %% [markdown]
# ### 描述器的实现及使用:纯装饰器的方式

# %%
from pycookbook.c8.c813checkattri_decro import *

f = typed(int)
display(f)

# %%
from pycookbook.c8.c813checkattri_decro import *

f = Integer('age')
display(f)


# %% tags=[]
from pycookbook.c8.c813checkattri_decro import *

print('expected: '+str(Integer))
if not 0:
    raise TypeError(f'expected: {repr(float)}')

# %% tags=[]
from pycookbook.c8.c813checkattri_decro import *

logging.basicConfig(level=logging.INFO)
class Stock3:
    age1 = UnsignedI1('age1')
    age2 = UnsignedI2('age2')

    def __init__(self,age1,age2):
        self.age1 = age1
        self.age2 = age2 

s3 = Stock3('hi',3.0)
display(s3.age1,s3.age2)

# %% [markdown]
# ## 单例模式 pycb C8.25
# ### 依然可以调用__init__()
# %%
from pycookbook.c8.c825singleton import Spam

s = Spam('hello')
s1 = Spam('hello')
display(s is s1)
display(list(Spam._spam_cache))
del s 
display(list(Spam._spam_cache))
del s1
display(list(Spam._spam_cache)) # 引用都售出后,在WeakValueDictionary中移除.

# %% [markdown]
# ### 隐藏__init__()

# %%
from pycookbook.c8.c825sing1 import Spam2

s = Spam2.get_instance('hello')
s1 = Spam2.get_instance('hello')
display(s is s1)

s = Spam2('hello') # __init__()出错.

# %% [markdown]
# ### 使用元类创建单例或单例的缓存 pycb C9.13
# 按关键字参数ids创建单例的缓存.
# %% 
from pycookbook.c8.c825sing2c913 import Spam3
s = Spam3('hello',42,ids=123)
s1 = Spam3('hello',42,ids=123)
s2 = Spam3('hello1',42,ids=123)
s3 = Spam3('hello',43,ids=456)
display(s is s1)
display(s1 is s2)
display(s is s3)
# %% [markdown]
# # chr/bytearray/Py3 编码

# %%
# 默认编码是unicode_escape
display(chr(97))
display(chr(0x61)) #0x61==97
display(ord('你'))
display(chr(20320))
display(chr(0x4f60))# 两个8位

# %%
display('abc'.encode('ascii'))
display('abc'.encode('utf-8'))
display('你好'.encode('utf-8'))
display('你好'.encode('unicode_escape'))

# %%
display(b'abc'.decode('ascii'))

# %%
from array import array

# typecode 不同,bytes()也不同
# b:1个byte / f:4个 / d:8个 / u:2个/
a = array('l',[3,4])
display(a)
b = bytes(a)
display(b)
x=3
x.to_bytes(8,'little')


# %%
b = bytes('hello world',encoding='iso8859-1')
display(b)
# 可见字节
b = bytes('hello world',encoding='ascii')
display(b,len(b))
b = bytes('你好',encoding='gbk')
display(b,len(b))
b = bytes('你好',encoding='utf-8')
display(b)

# %% [markdown]
#

# %%
