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
# 使用contextmanager

# %%

with couchdb("admin", "admin1", url="http://127.0.0.1:5984") as client:
    session = client.session()
    print("Username: {0}".format(session["userCtx"]["name"]))
    print("Databases: {0}".format(client.all_dbs()))
    selector = {"name": {"$eq": "JulesNew"}}
    result_c = test_db.get_query_result(selector)
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


# %%
