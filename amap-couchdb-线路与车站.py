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
# # amap+couchdb-线路/车站
# ## 共用代码

# %%
from amap.transportline import ptl_couchdb

# %% [markdown]
#  ### 共用调用函数前置代码
# %%
# buslines = '环路,100,101'
buslines = "环路,苦茶,100,101,100"
busline_df_column = [
    "id",
    "code",
    "type",
    "search_name",
    "key_name",
    "name",
    "front_name",
    "terminal_name",
    "company",
    "length",
    "status",
    "ic_card",
    "air",
    "total_price",
    "start_time",
    "end_time",
    "interval",
    "xs",
    "ys",
    "xs-84",
    "ys-84",
]
station_df_column = [
    "station_id",
    "name",
    "busline_id",
    "order",
    "poiid1",
    "xy_coords",
    "xy_coords_84",
    "poiid2",
    "poiid2_xy",
    "poiid2_xy_84",
]

# %% [markdown]
# 从CouchDB中来,到CouchDB中去
# %%
# try:
#     for busline_search_name in buslines.split(","):
#         result = getonetransportline_to_couchdb(busline_search_name, False)
#         line_result_dict[list(result.keys())[0]].append(list(result.values())[0])
# except KeyError as e:
#     print("Got a KeyError - reason %s" % str(e))
# for k, v in line_result_dict.items():
#     print("--查询线路结果类型:%s;数量%d;详情:%s" % (k, len(v), ",".join(v) if len(v) > 0 else "无此类线路结果."))
#     print("\n")
line_result_dict = ptl_couchdb.get_multitransportline_to_couchdb(buslines)
for k, v in line_result_dict.items():
    print("--查询线路结果类型:%s;数量%d;详情:%s" % (k, len(v), ",".join(v) if len(v) > 0 else "无此类线路结果."))
    print("\n")
