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
    # 网银交易类型
    extend_infos["online_trans_type"] = ""
    # 付款方银行编号
    extend_infos["bank_id"] = "01020000"
    # 卡类型
    extend_infos["card_type"] = "D"
    # 渠道号
    extend_infos["channel_no"] = "10000001"
    # 数字货币银行编号
    extend_infos["digital_bank_no"] = "01002"
    # 取现到账类型
    extend_infos["encash_type"] = "T0"
    # 场景类型
    extend_infos["pay_scene"] = "01"
    return extend_infos


class TestV2TradeFeecalcRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 手续费试算 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2TradeFeecalcRequest()
        request.huifu_id = "6666000116584429"
        request.req_date = ""
        request.req_seq_id = ""
        request.trade_type = "ENCASHMENT"
        request.trans_amt = "1000.00"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""