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
#   ### getonebusline-测试代码
#   测试用代码，取出一条线路具体内容并组装成dataframe。

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
#   ### getonebusline-方式1
#   重新定义getonebusline最好不要把dataframe当参数传递进去再返回.直接返回一条线路相关的内容在调用外边append会好一些.
#   函数说明：
#   1）每条线路的取正反向两条线路；
#   2）每条线路用高德地图busline唯一的id做关联
#   3）注意station有'poiid1','xy_coords','poiid2','poiid2_xy'，实际上同名称公交站点可能有多个，地理位置上离的也不远，不同线路的使用的站也不一样，poiid1是此线路中本站的实际具体位置。其中poiid2是某个名称的公交车站在地图上查找时返回的站点地址，可以理解成此名称的公交车站的代表，从高德poiid查找位置的api可以验证。

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
#   ### getonebusline-调用1

# %%
for busline_name in buslines.split(','):
    busline_df, station_df = getonebusline(busline_df, station_df,
                                           busline_name)
print('共有双向线路:%s条' % len(busline_df))
print(busline_df)
print('共有站点:%s个' % len(station_df))
print(station_df)


