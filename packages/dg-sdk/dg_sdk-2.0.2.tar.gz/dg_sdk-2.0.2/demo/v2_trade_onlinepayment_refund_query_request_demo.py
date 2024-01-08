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
    # 原退款全局流水号
    extend_infos["org_hf_seq_id"] = "0047default220818142809P500c0a8212f00000"
    # 原退款请求流水号
    extend_infos["org_req_seq_id"] = "1660804089"
    return extend_infos


class TestV2TradeOnlinepaymentRefundQueryRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 线上交易退款查询 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2TradeOnlinepaymentRefundQueryRequest()
        request.huifu_id = "6666000108854952"
        request.org_req_date = "20220818"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""