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
    # 银行编码
    extend_infos["bank_code"] = ""
    # 银行名称
    extend_infos["bank_name"] = ""
    # 是否启用
    extend_infos["bank_enable"] = ""
    return extend_infos


class TestV2TradeBankinstallmentinfoQueryRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 银行卡分期支持银行查询 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2TradeBankinstallmentinfoQueryRequest()
        request.page_num = "3"
        request.page_size = "1"
        request.product_id = "test"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""