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
    return extend_infos


class TestV2TradePaymentScanpayRefundqueryRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 交易退款查询接口 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2TradePaymentScanpayRefundqueryRequest()
        request.huifu_id = "6666000108854952"
        request.org_req_date = "20221110"
        request.org_hf_seq_id = "003100TOP2B221110093241P139ac139c0c00000"
        request.org_req_seq_id = ""
        request.mer_ord_id = ""

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""