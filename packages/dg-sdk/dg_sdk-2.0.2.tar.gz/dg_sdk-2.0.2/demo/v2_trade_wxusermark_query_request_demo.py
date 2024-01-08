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
    # 子商户公众账号ID
    extend_infos["sub_appid"] = "oQOa46X2FxRqEy6F4YmwIRCrA7Mk"
    # 渠道号
    extend_infos["channel_no"] = ""
    # 场景类型
    extend_infos["pay_scene"] = ""
    return extend_infos


class TestV2TradeWxusermarkQueryRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 微信用户标识查询接口 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2TradeWxusermarkQueryRequest()
        request.huifu_id = "6666000003100616"
        request.req_date = ""
        request.req_seq_id = ""
        request.auth_code = "130636925881320560"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""