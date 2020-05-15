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

# %%
test_db = client.create_database("test_db")
if test_db.exists():
    print("Success.")

# %%
document_key = "julia30"
julia30 = test_db.create_document({"_id": document_key, "name": "Jules", "age": 6})
if julia30.exists():
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
julia30 = test_db["julia30"]
print(type(julia30["name"]), type(julia30["age"]), type(julia30["pet"]))
print(julia30["pet"])
# %%
bob20 = julia30.copy()  # 实际上不用copy()
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
# 不仅修改,新增一列
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
tom21_doc = test_db["tom21"]
tom21_doc["_id"] = "tom24"
tom21_doc.save()
# %%
# 删除数据
# %% [markdown]
# ## Dealing with results

# %%
