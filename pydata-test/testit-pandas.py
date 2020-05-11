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
frame["new_year"], frame["new_pop"] = zip(*frame[["year", "pop"]].apply(new_value2, axis=1, args=("year", "pop")))
frame["new_year"], frame["new_pop"] = zip(*frame[["year", "pop"]].apply(new_value2, axis=1, year="year", pop="pop"))
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
        "origin": ["China", " China", "America", "China", "Thailand", "China", "america", "China", "China", "Japan"],
    }
)
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
tmp = list((product_small[df_isin]["product"])) if len((product_small[df_isin]["product"])) > 0 else []
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
# %%
product_new = pd.merge(product, product_1, on="id", how="inner")
product_new
# %%
product_new = pd.merge(product, product_1, on="id", how="right")
product_new

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
# TODO: 直接用left和right,不指定on实现两个集合左右差集
# %%
product_all = product_all.append(product_right, ignore_index=True)
product_all
# %%
product_all.drop_duplicates(product_right.columns.values, keep=False, inplace=True, ignore_index=True)
product_all
# %% [markdown]
# ### concat()的使用
# 可以理解成行或列的累加.
# %%
product_con1 = pd.concat([product, product_1], ignore_index=True)
product_con1
# %%
product_con1 = pd.concat([product, product_1], axis=1)
product_con1

# %%
# 按索引进行累加,理解axis和join的配对使用.
# axis=0时,由于两个df的列相同,inner和outer无差别;
# axis=1时,inner指的是按索引一致的进行累加.由原df按条件生成的新列进行累加新的列时有用.
product_1.loc[product_1["id"] == 110, "origin"] = "Japan"
product_con2 = pd.concat([product, product_1], axis=1, join="inner")
product_con2

# %%
# 动态计算新增1列,然后累加.
#  TODO:如果是一行代码动态新增2列呢?(代码中新增TODO时,加一个空格,否则在ipynb中不支持)
product_new_p = pd.DataFrame((x + "_new" for x in product_1["product"]), index=product_1.index, columns=["new_p"])
product_new_d = pd.DataFrame((x + "_new" for x in product_1["department"]), index=product_1.index, columns=["new_d"])
product_con3 = pd.concat([product_1, product_new_p, product_new_d], axis=1, join="inner")
product_con3
# %% [markdown]
# ### join()的使用

# %% [markdown]
# ## 数据的分组

# %% [markdown]
# ## 数据的选取

# %% [markdown]
# ## 数据的筛选

# %% [markdown]
# ## 数据的计数

# %% [markdown]
# ## 数据的统计值
