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
    # 原交易汇付全局流水号
    extend_infos["org_hf_seq_id"] = ""
    # 商户备注
    extend_infos["remark"] = "remark123"
    return extend_infos


class TestV2TradeOnlinepaymentBankpayPayerqueryRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 网银付款银行账户查询 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2TradeOnlinepaymentBankpayPayerqueryRequest()
        request.req_date = ""
        request.req_seq_id = ""
        request.huifu_id = "6666000003100615"
        request.org_req_date = "20221104"
        request.org_req_seq_id = "6246684562803777"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""