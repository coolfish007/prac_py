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
#  ## 公交线路详情及关联车站
#  通过高德地图，根据公交线路名称获取公交线路。

# %% [markdown]
#  ### 高德地图爬取的共用内容

# %%
import math
import time
import random
import requests
import pandas as pd
from openpyxl import load_workbook

# %%
headers = {
    'authority': 'ditu.amap.com',
    'accept': '*/*',
    'x-csrf-token': 'b20895a13b20f5e8e4b4a66ee5006bda',
    'x-requested-with': 'XMLHttpRequest',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
    'amapuuid': '1440c18d-8262-4b10-bf1d-dcfa90af7406',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://ditu.amap.com/search?query=%E7%8E%AF%E8%B7%AF&city=210100&geoobj=123.235132%7C41.790515%7C123.583626%7C41.961776&zoom=11.66',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cookie': 'UM_distinctid=1714efec5d91ad-0dcddda99ab246-396a7f06-fa000-1714efec5da7ca; cna=BEnxFtRzAkoCAXFCoBgfzgXk; CNZZDATA1255827602=412918052-1586405683-https%253A%252F%252Flbs.amap.com%252F%7C1586418799; _ga=GA1.2.1633570714.1587224095; passport_login=MzE2OTE2MSxhbWFwNW9mbjlkRVUsMnhsNzQzdXFqN2kzdmpyeXR6NWxjcWZieWd4MmZzemYsMTU4NzYxMTcxMixaVEJsTWpSa016UTBZelJqTldKall6WmtPVEJpWmpFeU4ySmtaR0V5TjJRPQ%3D%3D; oauth_state=ae8fa31ae280a2a0e644142c408b11cd; dev_help=Cm5hSMAkvpmaraCOySAMG2UwNDMyNTczMWE0OGI5ODIwNzIwYmViN2NjNmQ0NDE4N2E1NzZjMTUwMmRhNDlhMTQ3MzMwZjVhZmE4YTc5NTEus7mSrdBi1mHDTTh7gNwboXIGicOxRQcgdcUXFEULilQ2nc8zq%2BQ9cZkm1Nb3j0GTZnjb7yMdphosNOkRy%2F6ikMiSMXzZNCnLuZnVvfNkX4LBtvXzfH9D8hHbzRUHWbs%3D; guid=73b2-4fdc-b9ff-d417; x-csrf-token=b20895a13b20f5e8e4b4a66ee5006bda; CNZZDATA1255626299=500121251-1586274166-https%253A%252F%252Flbs.amap.com%252F%7C1588604569; l=eBPMb8PRQmIP7Q_bBO5Zhurza7793IdfcsPzaNbMiIHca1zPJFMJpNQcksVW6dtjgtCj5h-P8XiKbR3DJIzNwtrsywzdDt9x3xvR.; isg=BDc3615dJb7myKEODk0RW8eoxi2B_AteJmOE24nlwYZtOF96hsxXrtFaHphm0OPW',
    'if-none-match': 'W/"1b6f7-SoSjGUlTkPIxfxEeqavxip5gXtY"',
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
# ### 坐标转换的代码.
# TODO: 1.此函数放放在独立的包中.

# %%
pi = 3.1415926535897932384626  # π
a = 6378245.0  # 长半轴
ee = 0.00669342162296594323  # 扁率


def out_of_china(lng, lat):
    """
    判断是否在国内，不在国内不做偏移
    :param lng:
    :param lat:
    :return:
    """
    return not (lng > 73.66 and lng < 135.05 and lat > 3.86 and lat < 53.55)


def _transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
        0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * pi) + 40.0 *
            math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 *
            math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret


def _transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
        0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * pi) + 40.0 *
            math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 *
            math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret


def gcj02_to_wgs84(lng, lat):
    """
    GCJ02(火星坐标系)转GPS84
    :param lng:火星坐标系的经度
    :param lat:火星坐标系纬度
    :return:
    """
    if out_of_china(lng, lat):
        return lng, lat
    dlat = _transformlat(lng - 105.0, lat - 35.0)
    dlng = _transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [lng * 2 - mglng, lat * 2 - mglat]


# %% [markdown]
#  ### getonebusline-方式2
# TODO: 1.200505:line_no_info.txt的车站看一看json的数据结构.
# FIXME: 1.200505:公交线路应取所有而不是前两个.
# %%
def change_gcj02_in_busline(row, xs, ys):
    xs_value = row[xs]
    ys_value = row[ys]
    gcj02_lst = list(zip(map(float, xs_value.split(',')), map(float, ys_value.split(','))))
    wgs84_lst = []
    for coords in gcj02_lst:
        result = gcj02_to_wgs84(coords[0], coords[1])
        lng = str(round(result[0], 6))
        lat = str(round(result[1], 6))
        wgs84_lst.append((lng, lat))
    wgs84_lst = list(zip(*wgs84_lst))
    return ','.join(wgs84_lst[0]), ','.join(wgs84_lst[1])


def change_gcj02_in_station(row, xy_coords, poiid2_xy):
    xy_coords_value = list(map(float, row[xy_coords].split(';')))
    poiid2_xy_value = list(map(float, row[poiid2_xy].split(';')))
    result = gcj02_to_wgs84(xy_coords_value[0], xy_coords_value[1])
    xy_coords_84_lst = map(lambda v: str(round(v, 6)), result)
    xy_coords_84_str = ';'.join(xy_coords_84_lst)
    result = gcj02_to_wgs84(poiid2_xy_value[0], poiid2_xy_value[1])
    poiid2_xy_84_lst = map(lambda v: str(round(v, 6)), result)
    poiid2_xy_84_str = ';'.join(poiid2_xy_84_lst)
    return xy_coords_84_str, poiid2_xy_84_str


def change_gcj02_in_station2(row, xy_coords, poiid2_xy):
    xy_coords_value = list(map(float, row[xy_coords].split(';')))
    poiid2_xy_value = list(map(float, row[poiid2_xy].split(';')))
    result = gcj02_to_wgs84(xy_coords_value[0], xy_coords_value[1])
    xy_coords_84 = result
    result = gcj02_to_wgs84(poiid2_xy_value[0], poiid2_xy_value[1])
    poiid2_xy_84 = result
    return xy_coords_84, poiid2_xy_84


def getonebusline2(busline_name):
    busline_url = 'https://ditu.amap.com/service/poiInfo?keywords=' + busline_name
    response = requests.get(busline_url, headers=headers, params=params)
    data = response.json()
    busline = pd.DataFrame()
    oneline_stations = pd.DataFrame()
    if data['data']['message'] and data['data']['busline_list']:
        print('当前公交线路:[%s],地图已查询到.' % busline_name)
        busline_dict = data['data']['busline_list']
        if (len(busline_dict) >= 2):
            print('--抽取公交线路(双向):[%s]的详情' % busline_name)
            busline = pd.DataFrame(busline_dict, columns=busline_df_column)
            busline.loc[0, 'type'] = 'a2b'
            busline.loc[1, 'type'] = 'b2a'
            busline = busline[:2]
            busline['search_name'] = busline_name
            busline['xs-84'], busline['ys-84'] = zip(
                *busline[['xs', 'ys']].apply(change_gcj02_in_busline, axis=1, xs='xs', ys='ys'))
            i = 0
            while (i < 2):
                tmp = getbusstations(busline_dict[i], 'stations')
                print('--抽取公交线路:[%s-%s]的站点,此线路共有[%d]个站点' % (busline_name, busline.iloc[i]['type'], len(tmp)))
                # print(','.join(tmp['name']))
                tmp['busline_id'] = busline.iloc[i]['id']
                tmp['order'] = tmp.index
                tmp['xy_coords_84'], tmp['poiid2_xy_84'] = zip(
                    *tmp[['xy_coords', 'poiid2_xy']].apply(change_gcj02_in_station, axis=1, args=('xy_coords', 'poiid2_xy')))
                oneline_stations = oneline_stations.append(tmp, ignore_index=True)
                i += 1
    else:
        print('$$没有查询到公交线路:[%s]' % busline_name)
    return busline, oneline_stations


# %% [markdown]
# 写入excel文件,支持运行多次不断追加原excel文件的内容写入.
# TODO: 1.200505,考虑除excel其他存储形式的文件如parquet.
# %%
def write2excel(oldbusline, newbusline, oldstations, newstations):
    allbusline = oldbusline.append(newbusline, ignore_index=True)
    allstations = oldstations.append(newstations, ignore_index=True)
    allbusline.to_excel(writer, sheet_name=busline_sheet_name, header=True)
    allstations.to_excel(writer, sheet_name=stations_sheet_name, header=True)
    writer.save()
    writer.close()


# %% [markdown]
#  ### 共用调用函数前置代码
# %%
# buslines = '环路,100,101'
buslines = '环路,苦茶,100,101'
busline_df_column = [
    'id', 'code', 'type', 'search_name', 'key_name', 'name', 'front_name', 'terminal_name',
    'company', 'status', 'ic_card', 'air', 'total_price', 'start_time',
    'end_time', 'interval', 'xs', 'ys', 'xs-84', 'ys-84'
]
station_df_column = [
    'station_id', 'name', 'busline_id', 'order', 'poiid1', 'xy_coords', 'xy_coords_84', 'poiid2',
    'poiid2_xy', 'poiid2_xy_84'
]
busline_df = pd.DataFrame(columns=busline_df_column)
station_df = pd.DataFrame(columns=station_df_column)
line_noinfo = []


# %% [markdown]
# 从excel文件中读取线路名称,为了和下面代码兼容,组成字符串:'环路,101,100'的形式.

# %%
f_name = 'data/hgj_gong_jiao_xian_lu.xlsx'
book = load_workbook(f_name)
writer = pd.ExcelWriter(f_name, engine='openpyxl')
writer.book = book
writer.sheets = dict((ws.title, ws) for ws in book.worksheets)

busline_sheet_name = 'busline_info'
stations_sheet_name = 'stations_info'
busline_from_excel = pd.read_excel(f_name, sheet_name='hgj_gong_jiao_xian_lu')
oldbusline = pd.DataFrame()
oldstations = pd.DataFrame()
if(busline_sheet_name in writer.sheets):
    oldbusline = pd.read_excel(f_name, sheet_name=busline_sheet_name)
    oldstations = pd.read_excel(f_name, sheet_name=stations_sheet_name)

busline_lst = []
for bn in busline_from_excel['xian_lu_ming_cheng']:
    busline_lst.append(bn)
buslines = ','.join(busline_lst)
print(buslines)
# %% [markdown]
#  ### getonebusline-调用2
#  #  FIXME: 1.200505:抽取的线路append到结果时应去重.
# %%
try:
    exist_busline_lst = list(oldbusline['search_name'])
    for busline_name in buslines.split(','):
        if (busline_name in exist_busline_lst):
            print('--当前公交线路:[%s] 已存在--' % busline_name)
        else:
            busline, stations = getonebusline2(busline_name)
            if (len(busline) == 0):
                line_noinfo.append(busline_name)
            else:
                busline_df = busline_df.append(busline, ignore_index=True)
                station_df = station_df.append(stations, ignore_index=True)
        time.sleep(random.random() * random.randint(0, 7) + random.randint(0, 5))
except KeyError:
    print('--高德限制IP错误,以下是本次获取到的数据汇总:--')

print(station_df.head())
print(busline_df.head())
print('数据汇总:共需抽取[%d]条线路,已抽取到详情[%d]条线路,涉及站点: [%s] 个' %
      (len(buslines.split(',')), len(busline_df) / 2, len(station_df) / 2))
if(len(line_noinfo) > 0):
    print('共有: [%d] 条线路---没有详情---, 其线路名称:' % len(line_noinfo))
    print(','.join(line_noinfo))

write2excel(oldbusline, busline_df, oldstations, station_df)


# %%
