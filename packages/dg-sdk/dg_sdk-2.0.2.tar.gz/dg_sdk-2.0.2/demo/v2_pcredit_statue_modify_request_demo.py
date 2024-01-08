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
    # 开发者的应用ID
    extend_infos["app_id"] = "2021001153625042"
    return extend_infos


class TestV2PcreditStatueModifyRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 上架下架分期活动接口 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2PcreditStatueModifyRequest()
        request.req_seq_id = ""
        request.req_date = ""
        request.huifu_id = "6666000003117252"
        request.solution_id = "1456"
        request.status = "1"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""