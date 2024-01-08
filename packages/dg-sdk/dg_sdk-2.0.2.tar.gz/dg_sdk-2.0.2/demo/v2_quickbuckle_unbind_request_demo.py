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
    # 商户名称
    extend_infos["merch_name"] = "测试"
    return extend_infos


class TestV2QuickbuckleUnbindRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 新增快捷/代扣解绑接口 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2QuickbuckleUnbindRequest()
        request.req_date = ""
        request.req_seq_id = ""
        request.huifu_id = "6666000003078984"
        request.out_cust_id = "6666000103633606"
        request.token_no = "10000085852"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""