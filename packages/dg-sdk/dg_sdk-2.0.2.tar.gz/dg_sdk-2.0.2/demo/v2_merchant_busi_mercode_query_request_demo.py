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
    # 费率类型
    extend_infos["fee_type"] = "02"
    return extend_infos


class TestV2MerchantBusiMercodeQueryRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 商户微信支付宝ID查询 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2MerchantBusiMercodeQueryRequest()
        request.huifu_id = "6666000105013599"
        request.req_date = ""
        request.req_seq_id = ""
        request.pay_way = "A"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""