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
#     metadata:
#       interpreter:
#         hash: b217fd59a71bdcf8fc21cb9025cc5ba5b0ad4d40cbcd43f8e3bd181db5128951
#     name: 'Python 3.8.2 64-bit (''data'': venv)'
# ---

# %% [markdown]
# ## request+bs4

# %%
from IPython.display import display

# %%
import requests
from bs4 import BeautifulSoup

url = "https://gz.lianjia.com/ershoufang/"
page1 = requests.get(url)
display(page1)

# %%
bs_page = BeautifulSoup(page1.text, "lxml")
# houses = bs_page.find_all("div", class_="info clear")  # find_all
houses = bs_page.find_all("div", {"class": "info clear"})
house_one = houses[0]
print(house_one)

# %% [markdown]
# ### 使用bs4的节点选择器
# %%
house_info = house_one.find_all("div", {"class": "houseInfo"})
print(house_info)
position_info = house_one.find_all("div", {"class": "positionInfo"})
print(position_info)
totalPrice = house_one.find_all("div", class_="totalPrice")
print(totalPrice)
href = house_one.find_all("div", class_="title")
print(href)

# %%
import re

position_str = re.findall('_blank">(.+)</a.+_blank">(.+)?</a', str(position_info))
position_str = [item for item in position_str[0]]
print(position_str)

house_info_str = re.findall("span>(.+)?</div>", str(house_info))
house_info_str = str(house_info_str)[2:-2].split("|")  # 去掉[' 和 ']
print(house_info_str)

totalPrice_str = re.findall("<span>(.+)</span>(.+)</div>", str(totalPrice))
totalPrice_str = [item for item in totalPrice_str[0]]
print(totalPrice_str)
# totalPrice_str = list(totalPrice_str[0])

href_str = re.findall("http.+html", str(href))
print(href_str)

all_info = position_str + house_info_str + totalPrice_str + href_str
print(type(all_info), all_info)

# %%
from collections import defaultdict
import json

h_all_info_d = defaultdict(list)
posi_info_d = defaultdict(str)
posi_info_d["xiaoqu"] = position_str[0]
posi_info_d["quyu"] = position_str[1]
h_all_info_d["posi_info"] = posi_info_d
h_all_info_d["house_info"] = house_info_str  # 如果数据不用来分析,且在原始页面不确定内容,则不需要明确其key值
h_all_info_d["price_info"] = totalPrice_str
h_all_info_d["href_info"] = href_str
print(h_all_info_d)
h_all_info_json = json.dumps(h_all_info_d, ensure_ascii=False)
print(h_all_info_json)

# %% [markdown]
# ### 实验bs4的节点选择器的其他方法
# %%
print(bs_page.title.string, bs_page.script, bs_page.meta)  # 这种方法可以不用
print(type(bs_page.title))
print(house_one.contents)  # house_one的所有子节点内容,children返回生成器.
print(house_one.descendants)  # 所有子孙节点,每个节点是单独的元素,同样是生成器.
# %% [markdown]
# ### 使用bs4的CSS选择器
# %%
# %%
def hello(name=None, *addr, **kwargs):
    print(name, addr, kwargs)


def hello1(**kwargs):
    print(kwargs)


hello("a", "b", "c", 6, c=4, r=8)
# hello1({'e':1,'f':2}) #TypeError,{}会当成position arguments.
# %%

# %% [markdown]
# ## PyQuery
