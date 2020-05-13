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
# ### 创建一个数据库,插入数据

# %%

# %% [markdown]
# ### 更新数据

# %%

# %% [markdown]
# ### 使用已有数据库记录插入新数据

# %%

# %% [markdown]
# ### 使用已有数据库记录更新数据

# %%

# %% [markdown]
# ## 使用view

# %%
