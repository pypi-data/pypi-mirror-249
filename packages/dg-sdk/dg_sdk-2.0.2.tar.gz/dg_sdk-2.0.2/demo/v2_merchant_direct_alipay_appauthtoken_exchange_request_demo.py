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


class TestV2MerchantDirectAlipayAppauthtokenExchangeRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 支付宝直连-换取应用授权令牌 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2MerchantDirectAlipayAppauthtokenExchangeRequest()
        request.req_seq_id = ""
        request.req_date = ""
        request.huifu_id = "6666000103152205"
        request.app_id = "2021001153625042"
        request.oper_type = "1"
        request.app_auth_code = "123"
        request.app_auth_token = "202210100408496759"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""