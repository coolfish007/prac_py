# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # 沈阳公交线路和站点
# ## 公交线路
# 通过高德地图，根据公交线路名称获取公交线路。

# %%
import requests
import xlwt
import pandas as pd
from dx import dx


# %%
headers = {
    'authority': 'ditu.amap.com',
    'accept': '*/*',
    'x-csrf-token': 'e32efb46d464b024158d63446bab2507',
    'x-requested-with': 'XMLHttpRequest',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
    'amapuuid': '1440c18d-8262-4b10-bf1d-dcfa90af7406',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://ditu.amap.com/search?query=%E7%8E%AF%E8%B7%AF&city=210100&geoobj=123.099506%7C41.541332%7C124.198139%7C42.081772&zoom=10',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cookie': 'UM_distinctid=1714efec5d91ad-0dcddda99ab246-396a7f06-fa000-1714efec5da7ca; cna=BEnxFtRzAkoCAXFCoBgfzgXk; CNZZDATA1255827602=412918052-1586405683-https%253A%252F%252Flbs.amap.com%252F%7C1586418799; _ga=GA1.2.1633570714.1587224095; passport_login=MzE2OTE2MSxhbWFwNW9mbjlkRVUsMnhsNzQzdXFqN2kzdmpyeXR6NWxjcWZieWd4MmZzemYsMTU4NzYxMTcxMixaVEJsTWpSa016UTBZelJqTldKall6WmtPVEJpWmpFeU4ySmtaR0V5TjJRPQ%3D%3D; oauth_state=ae8fa31ae280a2a0e644142c408b11cd; dev_help=Cm5hSMAkvpmaraCOySAMG2UwNDMyNTczMWE0OGI5ODIwNzIwYmViN2NjNmQ0NDE4N2E1NzZjMTUwMmRhNDlhMTQ3MzMwZjVhZmE4YTc5NTEus7mSrdBi1mHDTTh7gNwboXIGicOxRQcgdcUXFEULilQ2nc8zq%2BQ9cZkm1Nb3j0GTZnjb7yMdphosNOkRy%2F6ikMiSMXzZNCnLuZnVvfNkX4LBtvXzfH9D8hHbzRUHWbs%3D; guid=e09f-1bb9-6767-1ccf; CNZZDATA1255626299=500121251-1586274166-https%253A%252F%252Flbs.amap.com%252F%7C1587997635; isg=BKurae7KcVTVCa0qegEl96ssOsmVwL9Cd2egtB0pe-p-vM4eqpKkk0FVEvzSnBc6; l=eBPMb8PRQmIP7g8-BO5N-urza77O6IdfCsPzaNbMiIHca1lAQi5S3NQc4R5vYdtjgtfmnExros38FRHJWkz3WjkDBeYQqVvu3op6-; x-csrf-token=e32efb46d464b024158d63446bab2507',
    'if-none-match': 'W/"1ba51-ACI7DeLNlcIM05GlLIxia0nDh6o"',
}

params = (
    ('query_type', 'TQUERY'),
    ('pagesize', '20'),
    ('pagenum', '1'),
    ('qii', 'true'),
    ('cluster_state', '5'),
    ('need_utd', 'true'),
    ('utd_sceneid', '1000'),
    ('div', 'PC1000'),
    ('addr_poi_merge', 'true'),
    ('is_classify', 'true'),
    ('zoom', '10'),
    ('city', '210100'),
    ('geoobj', '123.099506|41.541332|124.198139|42.081772'),
)


# %%
busline_name = '环路'
busline_df_column = [
    'id', 'code', 'key_name', 'name', 'front_name', 'terminal_name', 'company',
    'status', 'ic_card', 'air', 'total_price', 'start_time', 'end_time',
    'interval', 'xs', 'ys'
]
busline_df = pd.DataFrame(columns=busline_df_column)
busline_url = 'https://ditu.amap.com/service/poiInfo?keywords=' + busline_name
response = requests.get(busline_url, headers=headers, params=params)
data = response.json()


# %%
def getbusstations(busline_a2b, stations_key):
    stations_dict = busline_a2b[stations_key]
    print(stations_dict)


# %%
if data['data']['message'] and data['data']['busline_list']:
    print('公交线路%s精确命中: ' % busline_name)
    busline_a2b_dict = data['data']['busline_list'][0]
    sub = {key: busline_a2b_dict[key] for key in busline_df_column & busline_a2b_dict.keys()}
    busline_df = busline_df.append(sub, ignore_index=True)
    print(busline_df)
    getbusstations(busline_a2b_dict, 'stations')
