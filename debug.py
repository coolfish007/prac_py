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
def getbusstations(busline_dict, stations_key):
    stations_dict_list = busline_dict[stations_key]
    # print(type(stations_list))
    station_tmp = pd.DataFrame(stations_dict_list, columns=station_df_column)
    return station_tmp


# %%
def getonebusline(busline_df, station_df, data):
    print(len(busline_df))
    print(len(station_df))
    if data['data']['message'] and data['data']['busline_list']:
        # busline_dict = data['data']['busline_list'][0]
        # sub0 = {key: busline_dict[key] for key in busline_df_column & busline_dict.keys()}
        # busline_df = busline_df.append(sub0, ignore_index=True)
        busline_dict = data['data']['busline_list']
        if(len(busline_dict) >= 2):
            busline_df = busline_df.append(pd.DataFrame(busline_dict, columns=busline_df_column), ignore_index=True)
            busline_df.iloc[0]['type'] = 'a2b'
            busline_df.iloc[1]['type'] = 'b2a'
            busline_df = busline_df.iloc[:2]
            i = 0
            while(i < 2):
                station_tmp = getbusstations(busline_dict[i], 'stations')
                station_tmp['busline_id'] = busline_df.iloc[i]['id']
                station_tmp['order'] = station_tmp.index
                station_df = station_df.append(station_tmp, ignore_index=True)
                i += 1

        return busline_df, station_df


# %%
busline_name = '环路'
busline_df_column = [
    'id', 'code', 'type', 'key_name', 'name', 'front_name', 'terminal_name', 'company',
    'status', 'ic_card', 'air', 'total_price', 'start_time', 'end_time',
    'interval', 'xs', 'ys'
]
station_df_column = ['name', 'poiid1', 'xy_coords', 'poiid2', 'poiid2_xy', 'station_id']
busline_df = pd.DataFrame(columns=busline_df_column)
station_df = pd.DataFrame(columns=station_df_column)
busline_url = 'https://ditu.amap.com/service/poiInfo?keywords=' + busline_name
response = requests.get(busline_url, headers=headers, params=params)
data = response.json()
busline_df, station_df = getonebusline(busline_df, station_df, data)

busline_url = 'https://ditu.amap.com/service/poiInfo?keywords=100'
response = requests.get(busline_url, headers=headers, params=params)
data = response.json()
busline_df, station_df = getonebusline(busline_df, station_df, data)
print(busline_df)
print(station_df)
