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
#   kernelspec:
#     display_name: 'Python 3.8.2 64-bit (''data'': venv)'
#     language: python
#     name: python38264bitdatavenvaa4066e455544989bb855911b00b5f95
# ---

# %% [markdown]
#  # 沈阳公交线路和站点

# %% [markdown]
#  ## 公交线路详情及关联车站
#  通过高德地图，根据公交线路名称获取公交线路。

# %% [markdown]
#  ### 高德地图爬取的共用内容

# %%
import requests
import xlwt
import pandas as pd

# %%
headers = {
    'authority': 'ditu.amap.com',
    'accept': '*/*',
    'x-csrf-token': '611e34356f4e75a6b4fe490b72c2c7a6',
    'x-requested-with': 'XMLHttpRequest',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
    'amapuuid': '1440c18d-8262-4b10-bf1d-dcfa90af7406',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://ditu.amap.com/search?query=%E7%8E%AF%E8%B7%AF&city=210100&geoobj=123.395895%7C41.775079%7C123.459137%7C41.806199&zoom=14.12',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cookie': 'UM_distinctid=1714efec5d91ad-0dcddda99ab246-396a7f06-fa000-1714efec5da7ca; cna=BEnxFtRzAkoCAXFCoBgfzgXk; CNZZDATA1255827602=412918052-1586405683-https%253A%252F%252Flbs.amap.com%252F%7C1586418799; _ga=GA1.2.1633570714.1587224095; passport_login=MzE2OTE2MSxhbWFwNW9mbjlkRVUsMnhsNzQzdXFqN2kzdmpyeXR6NWxjcWZieWd4MmZzemYsMTU4NzYxMTcxMixaVEJsTWpSa016UTBZelJqTldKall6WmtPVEJpWmpFeU4ySmtaR0V5TjJRPQ%3D%3D; oauth_state=ae8fa31ae280a2a0e644142c408b11cd; dev_help=Cm5hSMAkvpmaraCOySAMG2UwNDMyNTczMWE0OGI5ODIwNzIwYmViN2NjNmQ0NDE4N2E1NzZjMTUwMmRhNDlhMTQ3MzMwZjVhZmE4YTc5NTEus7mSrdBi1mHDTTh7gNwboXIGicOxRQcgdcUXFEULilQ2nc8zq%2BQ9cZkm1Nb3j0GTZnjb7yMdphosNOkRy%2F6ikMiSMXzZNCnLuZnVvfNkX4LBtvXzfH9D8hHbzRUHWbs%3D; CNZZDATA1255626299=500121251-1586274166-https%253A%252F%252Flbs.amap.com%252F%7C1588249307; x-csrf-token=611e34356f4e75a6b4fe490b72c2c7a6; x5sec=7b22617365727665723b32223a223130633936393836383138333530326433646637303737313762623134353238434e6a4e752f5546454c50526c4976346a6f624a52673d3d227d; l=eBPMb8PRQmIP7Vk9BO5wPurza77OrHAjnsPzaNbMiIHcIsin5F4kDcgjMJomK4yA7HG5-tCXy9xP8XiKbRev-QaNwtrsywzdDt9xUxJO.; isg=BO3sjG0rT-L9wSus6PvLWfmW_I9nSiEcaM2O-S_kaQSzpltYlZse7Bg0lHpAJjnU',
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
    ('zoom', '14.12'),
    ('city', '210100'),
    ('geoobj', '123.395895|41.775079|123.459137|41.806199'),
)

# %% [markdown]
#  ### getbusstations


# %%
def getbusstations(busline_dict, stations_key):
    stations_dict_list = busline_dict[stations_key]
    # print(type(stations_list))
    # print('json中共有站点%s个:'%len(stations_dict_list))
    station_tmp = pd.DataFrame(stations_dict_list, columns=station_df_column)
    return station_tmp


# %% [markdown]
#  ### getonebusline-测试代码
#  测试用代码，取出一条线路具体内容并组装成dataframe。
# %%
busline_name = '环路'
busline_url = 'https://ditu.amap.com/service/poiInfo?keywords=' + busline_name
response = requests.get(busline_url, headers=headers, params=params)
data = response.json()
busline_df_column = [
    'id', 'code', 'type', 'key_name', 'name', 'front_name', 'terminal_name',
    'company', 'status', 'ic_card', 'air', 'total_price', 'start_time',
    'end_time', 'interval', 'xs', 'ys'
]
busline_df = pd.DataFrame(columns=busline_df_column)
busline_dict = data['data']['busline_list'][0]
sub0 = {
    key: busline_dict[key]
    for key in busline_df_column & busline_dict.keys()
}
busline_df = busline_df.append(sub0, ignore_index=True)
print(busline_df)

# %% [markdown]
#  ### getonebusline-方式1
#  重新定义getonebusline最好不要把dataframe当参数传递进去再返回.直接返回一条线路相关的内容在调用外边append会好一些.
#  函数说明：
#  1）每条线路的取正反向两条线路；
#  2）每条线路用高德地图busline唯一的id做关联
#  3）注意station有'poiid1','xy_coords','poiid2','poiid2_xy'，实际上同名称公交站点可能有多个，地理位置上离的也不远，不同线路的使用的站也不一样，poiid1是此线路中本站的实际具体位置。其中poiid2是某个名称的公交车站在地图上查找时返回的站点地址，可以理解成此名称的公交车站的代表，从高德poiid查找位置的api可以验证。


# %%
def getonebusline(busline_df, station_df, busline_name):
    busline_url = 'https://ditu.amap.com/service/poiInfo?keywords=' + busline_name
    response = requests.get(busline_url, headers=headers, params=params)
    data = response.json()
    if data['data']['message'] and data['data']['busline_list']:
        print('找到公交线路:%s' % busline_name)
        busline_dict = data['data']['busline_list']
        if (len(busline_dict) >= 2):
            print('开始抽取公交线路:%s的内容' % busline_name)
            tmp = pd.DataFrame(busline_dict, columns=busline_df_column)
            tmp.iloc[0]['type'] = 'a2b'
            tmp.iloc[1]['type'] = 'b2a'
            busline_df = busline_df.append(tmp[:2], ignore_index=True)
            i = 0
            while (i < 2):
                tmp = getbusstations(busline_dict[i], 'stations')
                tmp['busline_id'] = busline_df.iloc[i - 2]['id']
                tmp['order'] = tmp.index
                print('抽取公交线路:%s的站点,此线路共有%s个站点' % (busline_name, len(tmp)))
                station_df = station_df.append(tmp, ignore_index=True)
                i += 1
    return busline_df, station_df


# %% [markdown]
#  ### getonebusline-方式2
# %%
def getonebusline2(busline_name):
    busline_url = 'https://ditu.amap.com/service/poiInfo?keywords=' + busline_name
    response = requests.get(busline_url, headers=headers, params=params)
    data = response.json()
    busline = pd.DataFrame()
    oneline_stations = pd.DataFrame()
    if data['data']['message'] and data['data']['busline_list']:
        print('地图查询找到公交线路:[%s]' % busline_name)
        busline_dict = data['data']['busline_list']
        if (len(busline_dict) >= 2):
            print('抽取公交线路(双向):[%s]的详情' % busline_name)
            busline = pd.DataFrame(busline_dict, columns=busline_df_column)
            busline.iloc[0]['type'] = 'a2b'
            busline.iloc[1]['type'] = 'b2a'
            busline = busline[:2]
            i = 0
            while (i < 2):
                tmp = getbusstations(busline_dict[i], 'stations')
                print('抽取公交线路:[%s-%s]的站点,此线路共有[%s]个站点' %
                      (busline_name, busline.iloc[i]['type'], len(tmp)))
                tmp['busline_id'] = busline.iloc[i]['id']
                tmp['order'] = tmp.index
                oneline_stations = oneline_stations.append(tmp, ignore_index=True)
                i += 1
    else:
        print('地图---没有---查询找到公交线路:[%s]' % busline_name)
    return busline, oneline_stations


# %% [markdown]
#  ### 共用调用函数前置代码
# %%
# buslines = '环路,100,101'
buslines = '环路,苦茶,100,101'
busline_df_column = [
    'id', 'code', 'type', 'key_name', 'name', 'front_name', 'terminal_name',
    'company', 'status', 'ic_card', 'air', 'total_price', 'start_time',
    'end_time', 'interval', 'xs', 'ys'
]
station_df_column = [
    'name', 'busline_id', 'order', 'poiid1', 'xy_coords', 'poiid2',
    'poiid2_xy', 'station_id'
]
busline_df = pd.DataFrame(columns=busline_df_column)
station_df = pd.DataFrame(columns=station_df_column)
line_noinfo = []

# %% [markdown]
#  ### getonebusline-调用1

# %%
for busline_name in buslines.split(','):
    busline_df, station_df = getonebusline(busline_df, station_df,
                                           busline_name)
print('共有双向线路:%s条' % len(busline_df))
print(busline_df)
print('共有站点:%s个' % len(station_df))
print(station_df)

# %% [markdown]
#  ### getonebusline-调用2
# %%
for busline_name in buslines.split(','):
    busline, stations = getonebusline2(busline_name)
    if (len(busline) == 0):
        line_noinfo.append(busline_name)
    else:
        busline_df = busline_df.append(busline, ignore_index=True)
        station_df = station_df.append(stations, ignore_index=True)
print('共有双向线路: [%s] 条' % len(busline_df))
print(busline_df)
print('共有站点(双向): [%s] 个' % len(station_df))
print(station_df)
print('此次查询 [%d] 条线路的信息' % len(buslines.split(',')))
print('此次查询共有: [%d] 条线路没有详情, 其线路具体内容:' % len(line_noinfo))
print(','.join(i for i in line_noinfo))


# %%
