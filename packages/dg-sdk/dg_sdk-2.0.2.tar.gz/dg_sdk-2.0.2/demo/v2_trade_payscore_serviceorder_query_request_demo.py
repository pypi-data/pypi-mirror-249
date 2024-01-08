import unittest
import dg_sdk
import json
from demo.demo_config import *



def build_extend_infos():
    """
    非必填字段

    :return: 非必填字段组成的字典
    """
    extend_infos = dict()
    # 汇付服务订单号
    extend_infos["out_order_no"] = "1234323JKHDFE1243252"
    # 汇付全局流水号
    # extend_infos["org_hf_seq_id"] = ""
    # 请求流水号
    # extend_infos["org_req_seq_id"] = ""
    return extend_infos


class TestV2TradePayscoreServiceorderQueryRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 查询支付分订单 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2TradePayscoreServiceorderQueryRequest()
        request.huifu_id = "6666000108854952"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""