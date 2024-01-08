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
    # 备注
    extend_infos["remark"] = "标记123"
    return extend_infos


class TestV2TradeOnlinepaymentTransferRemittanceRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 汇付入账确认 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2TradeOnlinepaymentTransferRemittanceRequest()
        request.req_seq_id = ""
        request.req_date = ""
        request.huifu_id = "6666000106521787"
        request.trans_amt = "1019.00"
        request.notify_url = "http://C_TOPAT_NOTIFY"
        request.org_remittance_order_id = "20230214170030defaultit656505030"
        request.goods_desc = "商品描述001"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""