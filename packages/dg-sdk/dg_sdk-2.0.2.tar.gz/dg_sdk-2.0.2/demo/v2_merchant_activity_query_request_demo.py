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
    # 分页页码
    extend_infos["page_num"] = "1"
    # 分页条数
    extend_infos["page_size"] = "2"
    return extend_infos


class TestV2MerchantActivityQueryRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 商户活动报名查询 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2MerchantActivityQueryRequest()
        request.req_seq_id = ""
        request.req_date = ""
        request.huifu_id = "6666000103413615"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""