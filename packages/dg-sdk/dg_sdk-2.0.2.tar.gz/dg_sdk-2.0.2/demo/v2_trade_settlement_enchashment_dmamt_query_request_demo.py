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
    # 账户号
    extend_infos["acct_id"] = "F00598600"
    return extend_infos


class TestV2TradeSettlementEnchashmentDmamtQueryRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # DM取现额度查询 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2TradeSettlementEnchashmentDmamtQueryRequest()
        request.huifu_id = "6666000021291985"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""