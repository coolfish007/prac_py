import unittest
from amap.transportline import ptl_couchdb


class TestPtl_couchdb(unittest.TestCase):
    def test_get_multiline(self):
        buslines = "环路,苦茶,100,101,100"
        line_result_dict = ptl_couchdb.get_multitransportline_to_couchdb(buslines)
        for k, v in line_result_dict.items():
            print(
                "--查询线路结果类型:%s;数量%d;详情:%s" % (k, len(v), ",".join(v) if len(v) > 0 else "无此类线路结果.")
            )
            print("\n")


if __name__ == "__main__":
    unittest.main()
