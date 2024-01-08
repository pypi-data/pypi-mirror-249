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
    # extend_infos["acct_id"] = ""
    # 备注
    # extend_infos["remark"] = ""
    # 异步通知地址
    extend_infos["notify_url"] = "http://www.gangcai.com"
    return extend_infos


class TestV2TradeSettlementEnchashmentRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 取现接口 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2TradeSettlementEnchashmentRequest()
        request.req_date = ""
        request.req_seq_id = ""
        request.cash_amt = "0.01"
        request.huifu_id = "6666000021291985"
        request.into_acct_date_type = "T0"
        request.token_no = "10004053462"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""