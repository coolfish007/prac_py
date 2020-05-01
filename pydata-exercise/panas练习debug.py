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
