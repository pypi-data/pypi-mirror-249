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
    # 请求订单
    extend_infos["reqseqid_list"] = "[\"20221108104332293079\",\"20221108104817E93140\",\"20221108104800E93135\",\"20221108112153E93750\",\"20221108133737E96102\"]"
    return extend_infos


class TestV2TradeTransstatQueryRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 批量交易状态查询 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2TradeTransstatQueryRequest()
        request.huifu_id = "test"
        request.page_no = "1"
        request.page_size = "4"
        request.req_date = ""

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""