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
    # 每页条数
    extend_infos["page_size"] = "10"
    # 分页页码
    extend_infos["page_num"] = "1"
    # 账户号
    # extend_infos["acct_id"] = ""
    return extend_infos


class TestV2TradeAcctpaymentAcctlogQueryRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 账务流水查询 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2TradeAcctpaymentAcctlogQueryRequest()
        request.req_seq_id = ""
        request.huifu_id = "6666000108854952"
        request.acct_date = "20220816"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""