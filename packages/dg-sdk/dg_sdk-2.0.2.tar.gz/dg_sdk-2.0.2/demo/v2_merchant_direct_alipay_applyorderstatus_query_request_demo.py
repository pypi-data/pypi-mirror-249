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
    # 事务编号
    extend_infos["batch_no"] = "3123123"
    # 应用授权令牌
    extend_infos["app_auth_token"] = "201912BBecafff3696694c6d889503949a6adD18"
    return extend_infos


class TestV2MerchantDirectAlipayApplyorderstatusQueryRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 支付宝直连-查询申请状态 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2MerchantDirectAlipayApplyorderstatusQueryRequest()
        request.req_seq_id = ""
        request.req_date = ""
        request.huifu_id = "6666000003079710"
        request.app_id = "2019091967580486"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""