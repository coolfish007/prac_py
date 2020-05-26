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
# # Python(cloudant) 与 CouchDB

# %%
from cloudant.client import CouchDB
from cloudant import couchdb
from cloudant.document import Document
from requests.adapters import HTTPAdapter
import pandas as pd

# %% [markdown]
# ## 连接CouchDB

# %%
httpAdapter = HTTPAdapter(pool_connections=15, pool_maxsize=30)
client = CouchDB(
    "admin",
    "admin1",
    url="http://127.0.0.1:5984",
    connect=True,
    auto_renew=True,
    adapter=httpAdapter,
)
session = client.session()
print("Username: {0}".format(session["userCtx"]["name"]))
print("Databases: {0}".format(client.all_dbs()))
# client.disconnect()

# %% [markdown]
# ## 读取已有的数据库内容
# %%
# partitioned=True
a8684_db = client["sitemap-data-a8684-sy-test"]
doc_ids = []
for doc in a8684_db:
    print(doc["buslines"])
    bc_dict = doc["bl_info_company"][0]
    print(bc_dict["bl_info_company"])
    bstation_lst = doc["bl_sta_a2b"]
    if len(bstation_lst) > 0:
        station_df = pd.DataFrame(doc["bl_sta_a2b"])
        # print(station_df["bl_sta_a2b"])
        station_df["order"] = station_df.index + 1
        # print(station_df)
        stations_json = station_df.to_json(orient="index")
        print(stations_json)

# %% [markdown]
# ## 插入与更新数据

# %% [markdown]
# ### 创建一个数据库并新建数据
# client.crete_database(),创建一个新库时没有抛错.

# %%
test_db = client.create_database("test_db")
if test_db.exists():
    print("Success.")

# %%
document_key = "julia32"
julia = test_db.create_document({"_id": document_key, "name": "JulesNew", "age": 6})
if julia.exists():
    print("Create Successfully.")
# %% [markdown]
# ### 按key查询数据并更新
# julia30 = test_db["julia30"]
# print(julia30)
# julia30["pet"] = ["cat", "dog", "frog"]
# julia30["age"] = 8
# julia30.save()
# julia30["pet"] = ["cat", "dog", "frog"]
# julia30.save()
# %% [markdown]
# ### 查询(by key)新增删除数据
# %%
julia = test_db["julia30"]
print(julia)
print(type(julia["name"]), type(julia["age"]), type(julia["pet"]))
print(julia["pet"])
# %%
bob20 = julia.copy()  # 实际上不用copy()
bob20["_id"] = "bob20"
bob20["name"] = "bob"
bob20["age"] = 7
bob20_doc = test_db.create_document(bob20)
if bob20_doc.exists():
    print("Create bob sucessfully.")
# %%
tom21 = bob20
tom21["_id"] = "tom21"
tom21["name"] = "tom"
tom21["age"] = 7
tom21_doc = test_db.create_document(bob20)
if tom21_doc.exists():
    print("Create bob sucessfully.")

# %%
# 新增一列
john23 = bob20
john23["_id"] = "john23"
john23["name"] = "john"
john23["age"] = 7
john23["book"] = ["English", "math"]
john23_doc = test_db.create_document(bob20)
if john23_doc.exists():
    print("Create bob sucessfully.")

# %%
# 验证某列是否存在.并断开连接.
tom21_doc = test_db["tom21"]
print(type(tom21_doc))
print("tom's book:%s:" % ",".join(tom21_doc["book"])) if "book" in tom21_doc else print(
    "tom has no book."
)
client.disconnect()

# %%
# 重新连接
client.connect()
session = client.session()
print("Username: {0}".format(session["userCtx"]["name"]))
print("Databases: {0}".format(client.all_dbs()))
test_db = client["test_db"]
# %%
# 修改_id,直接新增一条记录,其他内容复制tom21_doc,有点意外.
tom = test_db["tom21"]
tom["_id"] = "tom24"
tom.save()

# %%
tom = test_db["tom24"]
tom["name"] = "tom24_new"
tom.save()
# %%
# 删除数据
julia = test_db["julia31"]
if julia.exists():
    print("julia31 exists.")
julia.delete()
julia = test_db["julia31"]
if not julia.exists():
    print("julia31 was deleted.")

# %% [markdown]
# ## Dealing with results

# %%
from cloudant.result import Result

# 什么排序规则?id,key的顺序,与控制台的顺序一致.
result_c = Result(test_db.all_docs, include_docs=True)
result = result_c[0]
# result 是list,结果可能是多个,里边嵌套的是dict.
print(type(result))
print(result)
result = result_c[5]
print(result)
result = result_c["julia30"]

print(type(result))
print("julia30:", result)

# %%
for result in result_c:
    # iterate 的对象是dict
    print(type(result))

# %%
selector = {"name": {"$eq": "Jules"}}
result_c = test_db.get_query_result(selector)
for result in result_c:

    print(type(result))
    # 构造新的doc然后更新
    update_doc = Document(test_db, result["_id"])
    # 这种写法是官方doc的写法.更新状态,避免否则报409,conflict的错误.看_rev的版本号.
    # 基本上是读出来的版本号往回写的时候要一致,否则会冲突.
    # 但是不推荐.
    # 实际作用是:result是dict,从result更新update_doc的值;_rev是附带的效果.
    update_doc.update(result)
    # 更新前,'_rev':'9-***'
    print(update_doc)
    update_doc["name"] = "julia30_new"
    # 更新后,数据库中的'_rev':'10-***'
    update_doc.save()

# %%
# 推荐这种写法,先修改值再在document中更新;
selector = {"name": {"$eq": "julia30_new"}}
result_c = test_db.get_query_result(selector)
for result in result_c:
    print(type(result))
    result["name"] = "julia30_new_2"
    # 构造新的doc然后更新
    update_doc = Document(test_db, result["_id"])
    update_doc.update(result)
    update_doc.save()


# %% [markdown]
# ## 使用contextmanager

# %%
with couchdb("admin", "admin1", url="http://127.0.0.1:5984") as client:
    session = client.session()
    print("Username: {0}".format(session["userCtx"]["name"]))
    print("Databases: {0}".format(client.all_dbs()))
    test_db = client["test_db"]
    selector = {"name": {"$eq": "JulesNew"}}
    result_c = test_db.get_query_result(selector)
    print(len(result_c.all()))
    for result in result_c:
        print(type(result))
        result["name"] = "juliaNew4"
        update_doc = Document(test_db, result["_id"])
        update_doc.update(result)
        update_doc.save()

# 出了context manager之后client就无效了.
# print("client disconnect:{0}".format(client.all_dbs()))

# %%
with couchdb("admin", "admin1", url="http://127.0.0.1:5984") as client:
    test_db = client.create_database("test_db")
    with Document(test_db, "tom26") as doc:
        doc["name"] = "tom26_new_" + doc.get("_rev") if doc.exists() else "tom26"
        doc["age"] = 10

# %% [markdown]
# ## dic的合并/dict 的value是list的合并;
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


# %%
