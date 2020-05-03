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
#     name: python38264bitdatavenv86c8e9e79e034983bf9e66a89847a1a4
# ---

# %% [markdown]
# 使用RestAPI获取POI（只用types获取）
# https://restapi.amap.com/v3/place/text?types=150500&city=2101&output=json&offset=100&page=1&key=0c5ccf69838f9de4ea0f118271c0f34f&extensions=all
#
# 使用
# https://www.amap.com/service/poiInfo?query_type=TQUERY&city=2101&keywords=地铁1号线

# %%
import requests
from pyecharts import options as opts
from pyecharts.charts import *
from pyecharts.commons.utils import JsCode

# headers信息 ,referer暂时不管
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
#           'Referer': 'https://sz.lianjia.com/ershoufang/'}


# %% [markdown]
# 以下header还没有运行成功过：

# %%
User_Agent = 'Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 ' \
    'Mobile/13B143 Safari/601.1'
Host = 'ditu.amap.com'
Accept = '* / *'
Accept_Encoding = 'gzip, deflate'
Accept_Language = 'en - US, en;q = 0.8, zh - CN;q = 0.6, zh;q = 0.4'
amapuuid = 'b51b4430 - 611e-421e - b5f0 - d4c0069ec83a'
Connection = 'keep - alive'
cookie = 'guid=62e9-7327-26e6-8630; UM_distinctid=15bf554ac5ce3-07d1fa60bf59d3-24414032-' \
    'cfcd8-15bf554ac5d163; _uab_collina=149446962066263280256309; passport_log' \
    'in=ODY0OTIzNTQsYW1hcEF1SUZSNU45MiwyN2ZiY2x4YjJicWN3NGZjb29qYWtuYTY4bjhpdDEzN' \
    'iwxNTA1Nzg4MDYzLE1XUm1OVE5oTlRRMk5tTmpOVEkwWWpWaU1EZzFNamRqTkdaaU5USmlabVk9; dev' \
    '_help=A31pORob9CZKI7Sru%2B22%2FGUwNWY0ZTEyMDMwOGZiZWIyMTUyNDg3N2M5NzdiNGY3NzVhNGF' \
    'iNDg5YzhjNjgzYmM5YjY5OTdmNjkxNjFlY2Y5%2BkDeYKdIYyjlQUymTgzjEbGZZwvhQT7HDehSDAbU71%' \
    '2BgMgS1RZws1VsgIqQbVPGtHubQVNo3jkPiGQcc4GgNzC%2BXgQLxYhEc7WDMILJBY%2FJWXDmjfTh8Wf8e' \
    'bkfF3VY%3D; key=bfe31f4e0fb231d29e1d3ce951e2c780; cna=HV1zEVpxFzkCATr4tPxil0OM; isg=At7' \
    'eZS1TC8m1jV8txoi1zUMNL33gNqN9in7_KohnSiEcq36F8C_yKQRJwY1Y; CNZZDATA1255626299=593' \
    '918092-1494468489-http%253A%252F%252Fwww.amap.com%252F%7C1505808643'
header = {}
header['User-Agent'] = User_Agent
header['Host'] = Host
header['Accept'] = Accept
header['Accept-Encoding'] = Accept_Encoding
header['Accept-Language'] = Accept_Language
header['amapuuid'] = amapuuid
header['Connection'] = Connection
header['cookie'] = cookie

# %% [markdown]
# 在chrome中F12，在network中，筛选poiinfo的request，copy成curl，在https://curl.trillworks.com/#
# 中进行转换，成下列内容,有时可以运行，有时被限制。

# %%
header = {
    'authority': 'ditu.amap.com',
    'accept': '*/*',
    'x-csrf-token': 'dbc38a03467e287e4b6af58f25dc1b1e',
    'x-requested-with': 'XMLHttpRequest',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
    'amapuuid': '1440c18d-8262-4b10-bf1d-dcfa90af7406',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://ditu.amap.com/search?id=B00141JKC4&city=440113&geoobj=112.615154%7C22.592179%7C114.565174%7C23.691503&query_type=IDQ&query=%E4%B8%87%E8%BE%BE%E5%B9%BF%E5%9C%BA(%E5%B9%BF%E5%B7%9E%E7%95%AA%E7%A6%BA%E5%BA%97)&zoom=9.51',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cookie': 'UM_distinctid=1714efec5d91ad-0dcddda99ab246-396a7f06-fa000-1714efec5da7ca; cna=BEnxFtRzAkoCAXFCoBgfzgXk; CNZZDATA1255827602=412918052-1586405683-https%253A%252F%252Flbs.amap.com%252F%7C1586418799; _ga=GA1.2.1633570714.1587224095; passport_login=MzE2OTE2MSxhbWFwNW9mbjlkRVUsMnhsNzQzdXFqN2kzdmpyeXR6NWxjcWZieWd4MmZzemYsMTU4NzYxMTcxMixaVEJsTWpSa016UTBZelJqTldKall6WmtPVEJpWmpFeU4ySmtaR0V5TjJRPQ%3D%3D; oauth_state=ae8fa31ae280a2a0e644142c408b11cd; dev_help=Cm5hSMAkvpmaraCOySAMG2UwNDMyNTczMWE0OGI5ODIwNzIwYmViN2NjNmQ0NDE4N2E1NzZjMTUwMmRhNDlhMTQ3MzMwZjVhZmE4YTc5NTEus7mSrdBi1mHDTTh7gNwboXIGicOxRQcgdcUXFEULilQ2nc8zq%2BQ9cZkm1Nb3j0GTZnjb7yMdphosNOkRy%2F6ikMiSMXzZNCnLuZnVvfNkX4LBtvXzfH9D8hHbzRUHWbs%3D; guid=a740-0e52-c664-4a3c; isg=BCUlCEMal4bAkfP04OMDYUEuNOdfYtn0L41IqycIRNxqPkWw-bLJxZofzKJIPvGs; l=eBPMb8PRQmIP7W-KBO5Znurza77tNQRb4sPzaNbMiIHca1rRFEArdNQc0E9wcdtjgtCbVhxzlhlyyRLHRnG-wxDDBy7i_2CxexvO.; x-csrf-token=dbc38a03467e287e4b6af58f25dc1b1e; CNZZDATA1255626299=500121251-1586274166-https%253A%252F%252Flbs.amap.com%252F%7C1587694496',
    'if-none-match': 'W/"127b-V2wlLjE7/0C6UdX3Qo/Xm6OV1co"',
}

# %% tags=["outputPrepend", "outputPrepend", "outputPrepend"]
subways = ['地铁1号线', '地铁2号线', '地铁9号线']
map_data = []
for sbw in subways:
    temp_list = []
    url = 'https://ditu.amap.com/service/poiInfo?query_type=TQUERY&city=2101&keywords={0}'.format(sbw)
    res = requests.get(url, headers=header)
    data = res.json()
    for item in data['data']['busline_list'][0]['stations']:
        x, y = item['xy_coords'].split(';')
        temp_list.append([float(x), float(y)])
    map_data.append(temp_list)
print(map_data)

# %%
bmap = BMap()
bmap.add_schema(
    # 需要申请一个AK
    baidu_ak='GNCdXmuXlZjj6MdsZG1lGIbkM8NF2qzs',
    # 地图缩放比例
    zoom=12,
    # 显示地图中心坐标点
    center=[123.44, 41.79],
    is_roam=True,
    map_style={
        "styleJson": [
            {
                "featureType": "water",
                "elementType": "all",
                "stylers": {"color": "#031628"},
            },
            {
                "featureType": "land",
                "elementType": "geometry",
                "stylers": {"color": "#000102"},
            },
            {
                "featureType": "highway",
                "elementType": "all",
                "stylers": {"visibility": "off"},
            },
            {
                "featureType": "arterial",
                "elementType": "geometry.fill",
                "stylers": {"color": "#000000"},
            },
            {
                "featureType": "arterial",
                "elementType": "geometry.stroke",
                "stylers": {"color": "#0b3d51"},
            },
            {
                "featureType": "local",
                "elementType": "geometry",
                "stylers": {"color": "#000000"},
            },
            {
                "featureType": "railway",
                "elementType": "geometry.fill",
                "stylers": {"color": "#000000"},
            },
            {
                "featureType": "railway",
                "elementType": "geometry.stroke",
                "stylers": {"color": "#08304b"},
            },
            {
                "featureType": "subway",
                "elementType": "geometry",
                "stylers": {"visibility": "off"},
            },
            {
                "featureType": "building",
                "elementType": "geometry.fill",
                "stylers": {"color": "#000000"},
            },
            {
                "featureType": "all",
                "elementType": "labels.text.fill",
                "stylers": {"color": "#d1dede"},
            },
            {
                "featureType": "all",
                "elementType": "labels.text.stroke",
                "stylers": {"color": "#000000"},
            },
            {
                "featureType": "building",
                "elementType": "geometry",
                "stylers": {"color": "#022338"},
            },
            {
                "featureType": "green",
                "elementType": "geometry",
                "stylers": {"color": "#062032"},
            },
            {
                "featureType": "boundary",
                "elementType": "all",
                "stylers": {"color": "#465b6c"},
            },
            {
                "featureType": "manmade",
                "elementType": "all",
                "stylers": {"color": "#022338"},
            },
            {
                "featureType": "label",
                "elementType": "all",
                "stylers": {"visibility": "off"},
            },
        ]
    },)

# 添加数据
colors = ['#e62739', '#7bc8a4', '#4cc3d9']
bmap.set_global_opts(legend_opts=opts.LegendOpts(
    textstyle_opts=opts.TextStyleOpts(color='#d1dede'), pos_left=10, pos_top=10))
for sub_data in map_data:
    bmap.add(subways[map_data.index(sub_data)],
            [sub_data],
            type_='lines',
            is_polyline=True,
            linestyle_opts=opts.LineStyleOpts(opacity=0.2, width=1, color=colors[map_data.index(sub_data)]),
            progressive=200,
            progressive_threshold=500,)

bmap.render('./charts/沈阳地铁.html')

# %%
