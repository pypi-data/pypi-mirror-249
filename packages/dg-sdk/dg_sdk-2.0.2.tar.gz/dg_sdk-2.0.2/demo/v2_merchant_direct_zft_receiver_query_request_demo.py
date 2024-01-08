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


class TestV2MerchantDirectZftReceiverQueryRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 直付通分账关系查询 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2MerchantDirectZftReceiverQueryRequest()
        request.req_seq_id = ""
        request.req_date = ""
        request.huifu_id = "6666000103518390"
        request.app_id = "2021002122659346"
        request.page_size = "2"
        request.page_num = "1"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""