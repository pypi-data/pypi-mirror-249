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
    # 原交易请求流水号
    extend_infos["org_req_seq_id"] = "202109187312431237001"
    # 原交易返回的全局流水号
    # extend_infos["org_hf_seq_id"] = ""
    return extend_infos


class TestV2TradePaymentScanpayClosequeryRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 交易关单查询接口 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2TradePaymentScanpayClosequeryRequest()
        request.req_date = ""
        request.req_seq_id = ""
        request.huifu_id = "6666000018328947"
        request.org_req_date = "20210918"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""