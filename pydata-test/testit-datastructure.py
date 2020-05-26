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
# ---

# %% [markdown]
# ## Dictionary

# %% [markdown]
# ### dic的合并

# %%
from collections import ChainMap
import itertools

result_dict = {"a": [], "b": [], "c": []}
result_a1 = {"a": "hello_a1"}
result = {"a": "hello_a2"}
result_b1 = {"b": "hello_b1"}
# 键值相同的只取第一个;
result_dict = dict(ChainMap(result_dict, result_a1, result))
print(result_dict)
# key值相同后边的覆盖前边的,注意这两种都把初始值的[]变为字符串了,数据结构变成保留的值了.
result_dict = dict(itertools.chain(result_dict.items(), result_a1.items(), result.items()))
print(result_dict)
# 键值对的turple组成的list,用使用list时先进行转型,不能直接[0]取值.
print(result_dict.items())  # dict_items([('a', 'hello_a2'), ('b', []), ('c', [])])
# 值是list会报错:TypeError: unhashable type: 'list'
# 键值相同的会被后者覆盖
result_dict = dict(result_a1.items() | result.items() | result_b1.items())
print(result_dict)
print(result_dict.keys())  # dict_keys(['a', 'b']),使用list也需要转型.

# %% [markdown]
# ### dict 的value是list的合并

# %%
result_dict = {"a": [], "b": [], "c": []}
result_a1 = {"a": "hello_a1"}
result = {"a": "hello_a2"}
key = list(result.keys())[0]
if key in result_dict:
    result_dict[key].append(list(result.values())[0])
else:
    result_dict.update(result)
result_dict
result = {"b": "hello_b1"}
key = list(result.keys())[0]
result_dict[key].append(list(result.values())[0]) if key in result_dict else result_dict.update(
    result
)
result = {"b": "hello_b2"}
key = list(result.keys())[0]
result_dict[key].append(list(result.values())[0]) if key in result_dict else result_dict.update(
    result
)
print(result_dict)
print(list(result_dict.items())[0][1])
print(result_dict.keys())
for k, v in result_dict.items():
    print("--查询线路结果类型:%s;数量:%d;详情:%s" % (k, len(v), ",".join(v if len(v) > 0 else "无.")))
    print("\n")
# %%
result_dict = {
    "duplicate_search": ["环路", "100", "100", "环路", "100", "101", "100"],
    "no_search_result": ["苦茶", "苦茶", "苦茶"],
    "ok_search_result": ["100", "101", "环路", "100", "101"],
}
for k, v in result_dict.items():
    print("--查询线路结果类型:%s;数量:%d;详情:%s" % (k, len(v), ",".join(v if len(v) > 0 else "无.")))
    print("\n")
