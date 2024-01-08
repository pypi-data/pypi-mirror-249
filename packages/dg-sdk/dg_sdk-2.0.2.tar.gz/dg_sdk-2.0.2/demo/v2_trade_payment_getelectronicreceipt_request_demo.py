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
    # 模板类型
    # extend_infos["template_type"] = ""
    # 是否分账
    # extend_infos["is_div"] = ""
    return extend_infos


class TestV2TradePaymentGetelectronicreceiptRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 电子回单查询 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2TradePaymentGetelectronicreceiptRequest()
        request.huifu_id = "6666000108840000"
        request.show_feemat = "1"
        request.org_hf_seq_id = ""
        request.org_req_date = "20220629"
        request.org_req_seq_id = "63124245672165376"
        request.pay_type = "ONLINE_PAY"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""