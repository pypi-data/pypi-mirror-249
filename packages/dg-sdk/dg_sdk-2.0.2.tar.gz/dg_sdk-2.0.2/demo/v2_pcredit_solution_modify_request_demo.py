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
    extend_infos["app_id"] = "2019090666961966"
    # 花呗分期商家贴息活动名称
    # extend_infos["activity_name"] = ""
    # 活动开始时间
    extend_infos["start_time"] = "2019-07-08 00:00:00"
    # 活动结束时间
    extend_infos["end_time"] = "2029-07-10 00:00:00"
    return extend_infos


class TestV2PcreditSolutionModifyRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 更新花呗分期方案 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2PcreditSolutionModifyRequest()
        request.req_seq_id = ""
        request.req_date = ""
        request.huifu_id = "6666000110468104"
        request.solution_id = "1515"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""