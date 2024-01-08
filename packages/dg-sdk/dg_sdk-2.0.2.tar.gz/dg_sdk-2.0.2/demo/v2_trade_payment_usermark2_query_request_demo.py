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
    # 银联支付标识
    extend_infos["app_up_identifier"] = "CloudPay"
    return extend_infos


class TestV2TradePaymentUsermark2QueryRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 获取银联用户标识接口 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2TradePaymentUsermark2QueryRequest()
        request.req_date = ""
        request.req_seq_id = ""
        request.huifu_id = "6666000018328947"
        request.auth_code = "6264664305553562612"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""