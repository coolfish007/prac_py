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
#     language: python
#     name: python38264bitdatavenvaa4066e455544989bb855911b00b5f95
# ---

# %%
# ms-python.python added
import os

try:
    os.chdir(os.path.join(os.getcwd(), "pydata-exercise"))
    print(os.getcwd())
except:
    pass

# %% [markdown]
#  ## Pandas 练习

# %%
import pandas as pd
import numpy as np
from openpyxl import load_workbook
from IPython.display import display

# %% [markdown]
#  ## 测试datafrmae传入的变化
#  传入的是调用的引用.
#  注意 `df=pd.DataFrame(a)`, 这句之后df就指向新的数据结构了,和传入的
#  df就没有关系了. 但是append操作必须返回才能起效果,不像drop(inplace=True).


# %%
def testdfgo(df):
    a = [{"A": 1, "B": 2}, {"A": 3, "B": 4}]
    print(df)
    # a = {'A': [1, 2], 'B': [3, 4]}
    # df = pd.DataFrame(a)
    df.append(a, ignore_index=True)
    print(df)
    df.drop(index=0, inplace=True)
    print(df)


df = pd.DataFrame([[0, 0], [5, 6]], columns=["A", "B"])
testdfgo(df)
print(df)


# %% [markdown]
#  ## dataframe apply()的使用
#  1)简单的操作最好使用向量化的方式;
#  2)复杂的操作使用apply(),如果使用lambda,分别对每列进行操作;df和column都可以使用apply()
#  3)如果同时对多列的数据联合操作,使用apply(),单独写一个函数进行操作;
#  4)不建议使用循环对pandas的行进行遍历;
# %% [markdown]
#  ### 处理每行的数据后并新增列

# %%
data = {
    "state": ["Ohio", "Ohio", "Ohio", "Nevada", "Nevada", "Nevada"],
    "year": [2000, 2001, 2002, 2001, 2002, 2003],
    "pop": [1.5, 1.7, 3.6, 2.4, 2.9, 3.2],
}
frame = pd.DataFrame(data)

# for row in frame.itertuples():
#    print(row)


def new_value0(row):
    return (5, 5)


def new_value(x=0, y=0):
    x = x + 5
    y = y * 5
    return x


def new_value1(row):
    row["new_year"] = row["year"] + 5
    row["new_pop"] = row["pop"] * 5
    return row


def new_value2(row, year, pop):
    x = row[year] + 5
    y = row[pop] * 5
    return x, y


# %%
frame["new_year"] = frame.apply(lambda row: row["year"] + 5, axis=1)
frame["new_year"] = frame.apply(lambda row: new_value(row["year"]), axis=1)


# %%
frame = frame.apply(new_value1, axis=1)
print(frame)


# %%
frame["new_year"], frame["new_pop"] = zip(*frame[["year", "pop"]].apply(new_value0, axis=1))
print(frame)

# %%
frame["new_year"], frame["new_pop"] = zip(
    *frame[["year", "pop"]].apply(new_value2, axis=1, args=("year", "pop"))
)
frame["new_year"], frame["new_pop"] = zip(
    *frame[["year", "pop"]].apply(new_value2, axis=1, year="year", pop="pop")
)
# print('result')
print(frame)


# %% [markdown]
#  ### 理解zip和unzip的使用

# %%
x1 = "5,6,7"
y1 = "1,2,3"
x1 = map(int, x1.split(","))
y1 = map(int, y1.split(","))
la = list(zip(x1, y1))
lb = []

for e in la:
    lb.append((e[0] + 1, e[1] + 1))

print(lb)
lb = list(zip(*lb))
print(lb)

# %% [markdown]
#  ## append()
#  主要是异常情况的处理
# %%
data = {
    "state": ["Ohio", "Ohio", "Ohio", "Nevada", "Nevada", "Nevada"],
    "year": [2000, 2001, 2002, 2001, 2002, 2003],
    "pop": [1.5, 1.7, 3.6, 2.4, 2.9, 3.2],
}
f_name = "../data/hgj_gong_jiao_xian_lu 4.xlsx"
frame = pd.DataFrame(data)
nan_frame = pd.DataFrame()

book = load_workbook(f_name)
writer = pd.ExcelWriter(f_name, engine="openpyxl")
writer.book = book
writer.sheets = dict((ws.title, ws) for ws in book.worksheets)

try:
    nan_frame = pd.read_excel(f_name, sheet_name="123")
except ValueError:
    print("无此数据")
except:
    print("其他异常")
nan_frame = nan_frame.append(frame, ignore_index=True)
print(nan_frame)

if "123" in writer.sheets:
    print("有此sheet页")
else:
    print("无此sheet页")
# %% [markdown]
# ## 初始化测试数据

# %%
product = pd.DataFrame(
    {
        "id": np.arange(101, 111),
        "date": pd.date_range(start="20200505", periods=10),
        "money": [5, 4, 65, 10, 15, 20, 35, 16, 6, 20],
        "product": ["苏打水", "可乐", "牛肉干", "老干妈", "菠萝", "冰激凌", "洗面奶", "洋葱", "牙膏", "薯片"],
        "department": ["饮料", "饮料", "零食", "调味品", "水果", np.nan, "日用品", "蔬菜", "日用品", "零食"],
        "origin": [
            "China",
            " China",
            "America",
            "China",
            "Thailand",
            "China",
            "america",
            "China",
            "China",
            "Japan",
        ],
    }
)
display(product)
# %%
product_1 = pd.DataFrame(
    {
        "id": np.arange(110, 113),
        "date": pd.date_range(start="20200514", periods=3),
        "money": [20, 7, 14],
        "product": ["薯片", "qiqudan", "cho"],
        "department": ["零食", "零食", "零食"],
        "origin": ["China", "China", "China"],
    }
)
product_1
# %% [markdown]
# ## 数据类型/行与列的理解
# PD的Series/NP的array,dtype/shape
# %%
pd.Series(["1", "1"]).values
print(pd.Series(["1", "1"]))
pd.Series(["1", "1"]).values.shape  # (2,) 一维,即一列.
print(pd.Series(["hello", "hello"], [2, 2]).reset_index())  # (2,),[2,2]是索引,不支持多维.

# pd.Series(["1", "1"], [1, 1], [3, 33]).values.shape  # (2,)   #此句出错.
np.array(pd.Series([[1, 1, 1], [2, 2, 2], ["hello", "hello"]]))  # 3个list,dtype=Object.
np.array(pd.Series([[1, 1, 1], [2, 2, 2], ["hello", "hello"]])).shape  # (3,)
np.array([["a", "a", "a", 1], ["b", "b", "b", 1]]).shape  # 2维(2,4),若行长度不一致,则由变为一维(2,)


# %%
# 其实增加列用合并函数挺麻烦的,不如在原df上使用赋值的方式新增列,避免循环.
# 这中间涉及行与列的思维转换,循环处理的是行,向量的方式处理的是列.所以上边的apply()需要用list的zip函数进行转换.
product_con3 = product_1.copy()
print((product_con3.info()))
print(type(product_con3["product"]))  # pandas的列是Series
print(product_con3["product"].dtypes)  # 数据类型是object,字符串以及混合的类型一般是object
print(product_con3["product"].apply(type))  # 查看此列每一个元素的类型,还可以新增一列显示类型
product_new_p = product_con3["product"] + "_new"
product_new_d = product_con3["department"] + "_new"
# 这是按列赋值OK,其实就是[][]=[列1][列2]的形式
product_con3["new_p"], product_con3["new_d"] = product_new_p, product_new_d
print(product_con3)
# [[]]的写法是二维的,需要用[[第一行两个值list],[第二行两个值],[第三行两个值]]的形式赋值,所以下面是错误的.
# product_con3[["new_p", "new_d"]] = [product_new_p, product_new_d]
print(product_new_p.values)  # ndarray,array(['薯片_new', 'qiqudan_new', 'cho_new'], dtype=object)
product_new_p.values.shape  # (3,)
# 对 ndarray的每个元素执行向量化操作
np.char.add(product_con3["money"].values.astype(str), "@2020")  # 强制转换类型
nda = np.char.split(product_new_p.values.astype(str), "_")
nda.shape  # (3,),每个元素type是list,值是:list(['薯片', 'new'])
print(nda[0])  # ['薯片', 'new']
print(list(zip(*nda[:])))
# %% [markdown]
# ## isin()的使用与数据类型
# 注意,数据类型不一致,特别是int和str, isin()无法正常匹配,merge()会抛错.
# %%
print(type(product))
print(type(product["product"]))
product.dtypes
redup = []
tmp = []
product_small = pd.DataFrame({"product": ["菠萝1", "qiqudan", "牛肉干1"], "money": ["15", "13", "65"]})
print(type(product_small["money"]))
# searched_stations = searched_stations.astype({"station_id": "int", "busline_id": "int"})
df_isin = product_small["money"].astype("int").isin(product["money"])
tmp = (
    list((product_small[df_isin]["product"]))
    if len((product_small[df_isin]["product"])) > 0
    else []
)
redup += tmp
redup += tmp
print(len(redup))
# %% [markdown]
#  ## 数据的合并
# %% [markdown] toc-hr-collapsed=true toc-hr-collapsed=true
#  ### merge()的使用
#  交集/并集/差集

# %% [markdown]
# #### merge()的on和how参数的用法
# merge()等同于SQL的join
# 如果想针对index进行比较合并,可以用join更简单,其默认行为就是针对index进行合并.
# 如果想对全列进行比较合并,可以用merge更简单,不指定on参数其其默认行为.
# 对某些列进行比较合并,用join更直接一些,无需明确指定left或right,按调用顺序来,注意在指定on之外进行set_index()操作.
# %%
# 针对id的inner merge,id匹配的行,除id外其两边的列都在结果中,没有的补Na
p_merge_inner_r = pd.merge(product, product_1, on="id", how="inner")
display(p_merge_inner_r)
p_merge = product_1.copy()
p_merge.loc[0, "origin"] = "Japan"
display(p_merge)
p_merge_inner_r = pd.merge(product, p_merge, on="id", how="inner")
display(p_merge_inner_r)
# %%
# 针对id的right merge,右边的行全列出,除id之外的两边的列都在结果中,没有的补Na.
p_merge_right_r = pd.merge(product, product_1, on="id", how="right")
display(p_merge_right_r)
# 想当然的想看一下针对index的right merge,一下这句是错误的,注意.
# p_merge_right_r = pd.merge(product, product_1, on="index", how="right")
# display(p_merge_right_r)

p_merge = product_1.copy()
p_merge.loc[0, "origin"] = "Japan"
display(p_merge)
# 以下的两个写法结果的值一样,只是左右不同.
# 此写法与on='id'的join效果一致.相当与右连接.
# on的参数多个列时,可以用['id','product']的方式.
p_merge_right_r = pd.merge(product, p_merge, on="id", how="right")
display(p_merge_right_r)
p_merge_right_r = pd.merge(p_merge, product, on="id", how="left")
display(p_merge_right_r)

# %% [markdown]
# #### 两个df的列相同时不指定on参数(有用)
# 对全column进行比较,相当于intersection(inner)和unioin(outer)
# 以及求差集
# %%
product_right = pd.merge(product, product_1, how="right")
product_right
# %% [markdown]
# 增加一列profit
# %%
product_2 = product_1.copy()
product_2["profit"] = 0.12
product_new = product.merge(product_2, how="right")
product_new
# %%
# 注意110的产地,一个是Japan,一个是China,merge的时候会当成不同数据
product_all = pd.merge(product, product_1, how="outer")
product_all
# %%
product_1.loc[product_1["id"] == 110, "origin"] = "Japan"
product_all = pd.merge(product, product_1, how="outer")
product_all
# %% [markdown]
# 注意drop_duplicates的用法,如果求差集,需要先创造重复后,再drop;
# 直接用left和right,不指定on实现两个集合左右差集
# %%
product_all = product_all.append(product_right, ignore_index=True)
product_all
# %%
product_all.drop_duplicates(
    product_right.columns.values, keep=False, inplace=True, ignore_index=True
)
product_all
# %% [markdown]
# ### concat()的使用
# 可以理解成行或列的累加.
# %%
# 按行简单累加,等同与append(),注意ignore_index
product_con1 = pd.concat([product, product_1], ignore_index=True)
product_con1
# %%
# 按列累加,没有的值补充Na
product_con1 = pd.concat([product, product_1], axis=1)
display(product_con1)
product_con1 = pd.concat([product_1, product], axis=1)
display(product_con1)

# %%
# 按索引进行累加,理解axis和join的配对使用.
# axis=0时,由于两个df的列相同,inner和outer无差别;
# axis=1时,inner指的是按索引一致的进行累加.由原df按条件生成的新列进行累加新的列时有用.
# 如果按匹配值进行合并操作,建议用merge或join,concat只进行累加.
product_1.loc[product_1["id"] == 110, "origin"] = "Japan"
product_con2 = pd.concat([product, product_1], axis=1, join="inner")
product_con2

# %%
# 动态计算新增1列,然后累加.
# 以下的写法并不推荐,建议直接对列的值向量化操作并赋值给新的列.
product_new_p = pd.DataFrame(
    (x + "_new" for x in product_1["product"]), index=product_1.index, columns=["new_p"]
)
product_new_d = pd.DataFrame(
    (x + "_new" for x in product_1["department"]), index=product_1.index, columns=["new_d"]
)
product_con3 = pd.concat([product_1, product_new_p, product_new_d], axis=1, join="inner")
product_con3
# %% [markdown]
# ### join()的使用
# %%
p_join = product.copy()
# display(p_join)  # 显示df的边框,from IPython.display import display
p1_join = product_1.copy()
# display(p1_join)
# 与merge()一样,默认对index进行操作.
# 结果中只有caller的行,以及两者所有列.
p1_join_r = p1_join.join(p_join, lsuffix="_caller", rsuffix="_right")
display(p1_join_r)

p1_join_on_r = p1_join.join(p_join.set_index("id"), on="id", lsuffix="_caller", rsuffix="_right")
display(p1_join_on_r)  # 默认是left,如果指定on,一定对被join df进行set_index()

# 只针对id进行inner join(),无论id外列的值是否相同,都会在结果中.
# 多列的写法如:on=['id','product']
# p1_join.loc[0, "origin"] = "Japan"
p1_join_on_inner_r = p1_join.join(
    p_join.set_index("id"), on="id", lsuffix="_caller", rsuffix="_right", how="inner"
)
display(p1_join_on_inner_r)


# %% [markdown]
# ## 数据的分组
# %%
p_bydepart = product.groupby("department")  # 注意返回的是df,index是department
display(p_bydepart.count().info())
display(p_bydepart.count()["money"])  # DataFrameGroupBy 没有可显示的内容,所以看count()
display(p_bydepart["money"].count())  # 这两者的写法一致


# %%
# DataFrameGroupBy是包装的对象,lazy,直到具体计算时才获取其具体值.
# One useful way to inspect a Pandas GroupBy object and see the splitting in
# action is to iterate over it. This is implemented in
# DataFrameGroupBy.__iter__() and produces an iterator of
# (group, DataFrame) pairs for DataFrames:
# split-apply-combine方法进行其中的数据处理.
display(p_bydepart.groups["零食"])  # 零食这一组包含的元素的index
display(product.loc[p_bydepart.groups["零食"]])  # 这一组还是员df的值
department, df = next(iter(p_bydepart))  # 迭代分组的第一个元素
display(department, df)  # 这个df就是某一组的dataframe
display(df["money"].count())  # 与上一个cell的['money']的'零食'计数一致

# %%
# 对分组的值进行基本的统计计算
display(p_bydepart["money"].size())  # 可以直接调用Series的方法或agg()聚合
# 对聚合的一个列应用不同的聚合函数
display(p_bydepart["money"].agg([len, np.sum, np.mean]))  # 数量(个数),算数和,算数平均值
# 对聚合的不同的列应用不同的聚合函数,字符串类型的product没有len方法.
display(p_bydepart.agg({"money": "sum", "product": "size"}))

p_bydepart = product.groupby(["department", "origin"]).count()
display(p_bydepart)

# %%
# 对分组进行apply()计算
# 实际上,以上的count()和各种计算都是apply()的方式

# %% [markdown]
# ## 数据的选取

# %% [markdown]
# ## 数据的筛选

# %% [markdown]
# ## 数据的计数

# %% [markdown]
# ## 数据的统计值
