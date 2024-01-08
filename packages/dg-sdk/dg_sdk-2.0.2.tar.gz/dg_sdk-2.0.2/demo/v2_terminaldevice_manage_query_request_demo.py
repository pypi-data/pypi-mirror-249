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
    # 渠道商号
    extend_infos["upper_huifu_id"] = "6666000104633228"
    # 终端号
    # extend_infos["deviceId"] = ""
    # 绑定状态
    extend_infos["is_bind"] = "Y"
    # 当前页码
    extend_infos["page_num"] = "1"
    # 每页条数
    extend_infos["page_size"] = "1"
    return extend_infos


class TestV2TerminaldeviceManageQueryRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 服务商终端列表查询 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2TerminaldeviceManageQueryRequest()
        request.req_seq_id = ""
        request.req_date = ""

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""