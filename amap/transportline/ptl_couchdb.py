""" 
TODO: 
"""
__author__ = "coolfish007"


import time
import json
import requests
from cloudant import couchdb
from cloudant.document import Document
from ._amap_request_params import headers, params


NO_SEARCH_RESULT = "no_search_result"
DUPLICATE_SEARCH = "duplicate_search"
OK_SEARCH_RESULT = "ok_search_result"
COUCHDB_URL = "http://127.0.0.1:5984"
COUCHDB_USER = "admin"
COUCHDB_PW = "admin1"
AMAP_POIINFO_URL_PREFIX = "https://ditu.amap.com/service/poiInfo?keywords="
line_result_dict = {NO_SEARCH_RESULT: [], DUPLICATE_SEARCH: [], OK_SEARCH_RESULT: []}

# headers = {
#     "authority": "ditu.amap.com",
#     "accept": "*/*",
#     "x-csrf-token": "b20895a13b20f5e8e4b4a66ee5006bda",
#     "x-requested-with": "XMLHttpRequest",
#     "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
#     "amapuuid": "1440c18d-8262-4b10-bf1d-dcfa90af7406",
#     "sec-fetch-site": "same-origin",
#     "sec-fetch-mode": "cors",
#     "sec-fetch-dest": "empty",
#     "referer": "https://ditu.amap.com/search?query=%E7%8E%AF%E8%B7%AF&city=210100&geoobj=123.235132%7C41.790515%7C123.583626%7C41.961776&zoom=11.66",
#     "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
#     "cookie": "UM_distinctid=1714efec5d91ad-0dcddda99ab246-396a7f06-fa000-1714efec5da7ca; cna=BEnxFtRzAkoCAXFCoBgfzgXk; CNZZDATA1255827602=412918052-1586405683-https%253A%252F%252Flbs.amap.com%252F%7C1586418799; _ga=GA1.2.1633570714.1587224095; passport_login=MzE2OTE2MSxhbWFwNW9mbjlkRVUsMnhsNzQzdXFqN2kzdmpyeXR6NWxjcWZieWd4MmZzemYsMTU4NzYxMTcxMixaVEJsTWpSa016UTBZelJqTldKall6WmtPVEJpWmpFeU4ySmtaR0V5TjJRPQ%3D%3D; oauth_state=ae8fa31ae280a2a0e644142c408b11cd; dev_help=Cm5hSMAkvpmaraCOySAMG2UwNDMyNTczMWE0OGI5ODIwNzIwYmViN2NjNmQ0NDE4N2E1NzZjMTUwMmRhNDlhMTQ3MzMwZjVhZmE4YTc5NTEus7mSrdBi1mHDTTh7gNwboXIGicOxRQcgdcUXFEULilQ2nc8zq%2BQ9cZkm1Nb3j0GTZnjb7yMdphosNOkRy%2F6ikMiSMXzZNCnLuZnVvfNkX4LBtvXzfH9D8hHbzRUHWbs%3D; guid=73b2-4fdc-b9ff-d417; x-csrf-token=b20895a13b20f5e8e4b4a66ee5006bda; CNZZDATA1255626299=500121251-1586274166-https%253A%252F%252Flbs.amap.com%252F%7C1588604569; l=eBPMb8PRQmIP7Q_bBO5Zhurza7793IdfcsPzaNbMiIHca1zPJFMJpNQcksVW6dtjgtCj5h-P8XiKbR3DJIzNwtrsywzdDt9x3xvR.; isg=BDc3615dJb7myKEODk0RW8eoxi2B_AteJmOE24nlwYZtOF96hsxXrtFaHphm0OPW",
#     "if-none-match": 'W/"1b6f7-SoSjGUlTkPIxfxEeqavxip5gXtY"',
# }

# params = (
#     ("query_type", "TQUERY"),
#     ("pagesize", "20"),
#     ("pagenum", "1"),
#     ("qii", "true"),
#     ("cluster_state", "5"),
#     ("need_utd", "true"),
#     ("utd_sceneid", "1000"),
#     ("div", "PC1000"),
#     ("addr_poi_merge", "true"),
#     ("is_classify", "true"),
#     ("zoom", "14.12"),
#     ("city", "210100"),
#     ("geoobj", "123.395895|41.775079|123.459137|41.806199"),
# )


def getonebusline_from_amap(busline_search_name):
    # data = {"busline": "amap_KeyError"}
    busline_url = AMAP_POIINFO_URL_PREFIX + busline_search_name
    response = requests.get(busline_url, headers=headers, params=params)
    amap_result = response.json()
    if "data" not in amap_result:
        print("--高德限制IP错误, 查询名称: {0} --".format(busline_search_name))
        raise KeyError(amap_result)
    else:
        return amap_result


def get_onetransportline_to_couchdb(busline_search_name, from_8684):
    selector_key = "name_in_8684" if from_8684 else "search_name"
    selector = {selector_key: {"$eq": busline_search_name}}
    with couchdb(COUCHDB_USER, COUCHDB_PW, url=COUCHDB_URL) as client:
        amap_transport_db = client.create_database("amap_transport_line")
        result_list = amap_transport_db.get_query_result(selector).all()
        if len(result_list) == 0:
            data = getonebusline_from_amap(busline_search_name)
            if data["data"]["message"] and data["data"]["busline_list"]:
                transport_line_list = data["data"]["busline_list"]
                for line_dict in transport_line_list:
                    with Document(amap_transport_db, line_dict["id"]) as doc:
                        if not doc.exists():
                            doc["search_name"] = busline_search_name
                            doc["name_in_8684"] = busline_search_name
                            doc["name_in_amap"] = line_dict["name"]
                            doc["amap_busline_info"] = json.dumps(line_dict)
                            doc["insert_datetime"] = time.strftime(
                                "%Y-%m-%d %H:%M:%S", time.localtime(time.time())
                            )
                            doc["update_datetime"] = "0"
                        else:
                            # 高德地图的线路内容更新
                            pass
                return {OK_SEARCH_RESULT: busline_search_name}
            else:
                return {NO_SEARCH_RESULT: busline_search_name}
        else:
            return {DUPLICATE_SEARCH: busline_search_name}


def get_multitransportline_to_couchdb(busline_search_str):
    for busline_search_name in busline_search_str.split(","):
        result = get_onetransportline_to_couchdb(busline_search_name, False)
        line_result_dict[list(result.keys())[0]].append(list(result.values())[0])

    # for k, v in line_result_dict.items():
    #     print("--查询线路结果类型:%s;数量%d;详情:%s" % (k, len(v), ",".join(v) if len(v) > 0 else "无此类线路结果."))
    #     print("\n")

    return line_result_dict


if __name__ == "__main__":
    pass
