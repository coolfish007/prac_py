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
print(page1)

# %%
bs_page = BeautifulSoup(page1.text, "lxml")
# houses = bs_page.find_all("div", class_="info clear")  # find_all
houses = bs_page.find_all("div", {"class": "info clear"})
print(len(houses))
house_one = houses[0]
print(house_one)

# %% [markdown]
# ### 使用bs4的方法选择器
# 一个完整的实例,使用方法选择器(API)+正则表达式.
# 查找到返回的都是列表ResultSet,注意这里和pyquery最大的区别.
# 使用resultset,需要随处列表和其中的元素进行操作,很繁复.
# %%
house_info = house_one.find_all("div", {"class": "houseInfo"})
print(type(house_info), house_info)
print("*" * 5)
print(str(house_info))
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
# ### 实验bs4的节点选择器

# %%
# house_info,使用节点选择器,不使用正则表达式提取信息.
# 所以,这种使用find_all(纯API的方式解析)之后必然使用大量的循环以及正则表达式.
# 灵活提前信息需使用bs4的CSS或XPath,chrome等浏览器右键copy进行选择.
# 以下是houseInfo节点下的内容:虽然只有一个houseInfo,但也要对list进行操作
""" 
<div class="houseInfo"><span class="houseIcon"></span>
2室1厅 | 81.44平米 | 南 | 毛坯 | 中楼层(共11层)  | 塔楼</div>
"""
print(type(house_info[0]), house_info[0].descendants)
for item in house_info[0].descendants:
    print(type(item), item)  # 遍历,但要提前信息的话,需要判断不同的节点类型,很麻烦.
print(
    house_info[0].name, house_info[0].string, house_info[0].get_text()
)  # 这种情况获取不到内容,为NavigableString,为None,可改为调用get_text()

# %%
print(bs_page.title.string, bs_page.script, bs_page.meta)  # 这种方法可以不用
print(type(bs_page.title))
print(house_one.contents)  # house_one的所有直接子节点内容,返回列表..children返回内容一样,类型是生成器.
print(house_one.descendants)  # 递归子孙节点,每个节点是单独的元素,同样是生成器.

# %%
print(house_one.parent)  # parent节点的所有内容(包含本节点).parents递归获取所有祖先节点,.
print(house_one.attrs["class"])  # ['info','clear'],两个值

# %% [markdown]
# ### 使用bs4的CSS选择器
# 以house_one为例,select 返回的也是ResultSet,只有
# %%
print(type(bs_page))
houses = bs_page.select("div.info.clear")
print(len(houses))
house_one = houses[0]
print(type(house_one), house_one)

# %%
house_info = house_one.select(".houseInfo")  # 每次查找都是ResultSet
print(type(house_info[0]), house_info[0])  # 取出的第一个元素是Tag
print(house_info[0].get_text())  # 调用.string返回None,调用.get_text()放回值

# %%
position_info = house_one.select(".positionInfo")[0]
print(type(position_info), position_info)
tmp = position_info.select("a:nth-child(2)")[0]
print(type(tmp), tmp.string)  # 取得小区名称
tmp = position_info.select("a:nth-of-type(2)")[0]
print(type(tmp), tmp.string)  # 取得区域名称
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
# 使用CSS选择器对节点的遍历和查找,返回的都是PyQuery类型
#
# %%
from pyquery import PyQuery as pq

pq_page = pq(url)  # TODO:更多参数的使用

# %%
houses = pq_page("div.info.clear")
print(type(houses), len(houses))  # PyQuery

# %%
house_one = next(houses.items())
# %%
print(type(house_one), house_one)  # 返回的都是PyQuery
house_info = house_one(".houseInfo")
print(house_info.text())  # 提取文本值,2室1厅 | 81.44平米 | 南 | 毛坯 | 中楼层(共11层) | 塔楼
tmp = house_info.parent().parent()
print(tmp == house_one)  # True
# %%
position_info = house_one(".positionInfo")
# 注意起调的元素是position_info
xq = position_info("a:nth-child(2)")  # 仁安花园,首先是a元素,其次是第二个元素,如果第二个元素不是a,那么什么都不返回.
print(xq.text())
qy = position_info("a:nth-of-type(2)")  # 朱村,第二个a元素
print(qy.text())

# %%
# 使用text()需要小心.text()提取的是所有文本内容,例如positionInfo:
""" <div class="positionInfo"><span class="positionIcon"></span>
<a href="https://gz.lianjia.com/xiaoqu/2111103316435/" target="_blank" data-log_index="1" data-el="region">中海名都 </a>
   -  <a href="https://gz.lianjia.com/ershoufang/binjiangzhong/" target="_blank">滨江中</a> 
   </div> 
"""
print(position_info.text())  # 返回:中海名都 - 滨江中(每个文本应该都trim过),如果这个示例中<span>节点有文本,也会获取到,如下:
position_info.find("span").text("add content to span ")
print(position_info.text())
position_info("span").remove()  # 移除<span>节点
print(position_info.text())


# %% [markdown]
### 使用API查找节点
# 以house_one为例
# %%
house_info = house_one.find(".houseInfo")  # 查找范围是所有子孙节点.与house_one(".houseInfo")一致.
print(type(house_info), house_info)
print(house_info.html())  # html以及文本的内容.
tmp = house_info.parents(".info.clear")
print(tmp.attr("class"))  # 提取属性
print(tmp == house_one)  # True
# %%
