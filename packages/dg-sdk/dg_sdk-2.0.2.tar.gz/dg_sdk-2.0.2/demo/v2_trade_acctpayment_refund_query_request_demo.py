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


class TestV2TradeAcctpaymentRefundQueryRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 余额支付退款查询 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2TradeAcctpaymentRefundQueryRequest()
        request.org_req_seq_id = "20211021787214848332"
        request.org_req_date = "20211021"
        request.huifu_id = "6666000018344461"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""