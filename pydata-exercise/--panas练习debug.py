# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
# ms-python.python added
import os
try:
    os.chdir(os.path.join(os.getcwd(), 'pydata-exercise'))
    print(os.getcwd())
except:
    pass
# %% [markdown]
# ## Pandas 练习

# %%
import pandas as pd

# %% [markdown]
# ## 测试datafrmae传入的变化
# 传入的是调用的引用.
# 注意 `df=pd.DataFrame(a)`, 这句之后df就指向新的数据结构了,和传入的
# df就没有关系了. 但是append操作必须返回才能起效果,不像drop(inplace=True).


# %%
def testdfgo(df):
    a = [{'A': 1, 'B': 2}, {'A': 3, 'B': 4}]
    print(df)
    # a = {'A': [1, 2], 'B': [3, 4]}
    # df = pd.DataFrame(a)
    df.append(a, ignore_index=True)
    print(df)
    df.drop(index=0, inplace=True)
    print(df)


df = pd.DataFrame([[0, 0], [5, 6]], columns=['A', 'B'])
testdfgo(df)
print(df)

# %% [markdown]
# ## datafrmae apply函数,每行的数据处理后并新增列
# %%
data = {
    'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada', 'Nevada'],
    'year': [2000, 2001, 2002, 2001, 2002, 2003],
    'pop': [1.5, 1.7, 3.6, 2.4, 2.9, 3.2]
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
    row['new_year'] = row['year'] + 5
    row['new_pop'] = row['pop'] * 5
    return row


def new_value2(row, year, pop):
    x = row[year] + 5
    y = row[pop] * 5
    return x, y


# %%
frame['new_year'] = frame.apply(lambda row: row['year'] + 5, axis=1)
frame['new_year'] = frame.apply(lambda row: new_value(row['year']), axis=1)

# %%
frame = frame.apply(new_value1, axis=1)
print(frame)

# %%
frame['new_year'], frame['new_pop'] = zip(
    *frame[['year', 'pop']].apply(new_value0, axis=1))
print(frame)
# %%
frame['new_year'], frame['new_pop'] = zip(
    *frame[['year', 'pop']].apply(new_value2, axis=1, args=('year', 'pop')))
frame['new_year'], frame['new_pop'] = zip(
    *frame[['year', 'pop']].apply(new_value2, axis=1, year='year', pop='pop'))
print(frame)

# %% [markdown]
# 理解zip和unzip的使用
# %%
x1 = '5,6,7'
y1 = '1,2,3'
x1 = map(int, x1.split(','))
y1 = map(int, y1.split(','))
la = list(zip(x1, y1))
lb = []

for e in la:
    lb.append((e[0]+1, e[1]+1))

print(lb)
lb = list(zip(*lb))
print(lb)
# %%
