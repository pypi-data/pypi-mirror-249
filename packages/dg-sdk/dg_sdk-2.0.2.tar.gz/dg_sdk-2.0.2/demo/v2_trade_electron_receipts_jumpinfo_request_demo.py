import unittest
import dg_sdk
import json
from demo.demo_config import *


def getReceiptDataRucan():
    dto = dict()
    # 三方通道类型
    dto["third_channel_type"] = "T"
    # 微信票据信息
    dto["wx_receipt_data"] = getWxReceiptDataRucan()

    return json.dumps(dto)

def getWxReceiptDataRucan():
    dto = dict()
    # 跳转信息
    dto["jump_info"] = getJumpInfo()

    return dto;

def getJumpInfo():
    dto = dict()
    # 小票跳转信息小程序AppID
    dto["merchant_app_id"] = "wxcaced8415a866378"
    # 小票跳转信息小程序路径
    dto["merchant_path"] = "pages/cashier/paySuccess"

    return dto;


def build_extend_infos():
    """
    非必填字段

    :return: 非必填字段组成的字典
    """
    extend_infos = dict()
    return extend_infos


class TestV2TradeElectronReceiptsJumpinfoRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 跳转电子小票页面 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2TradeElectronReceiptsJumpinfoRequest()
        request.req_seq_id = ""
        request.req_date = ""
        request.huifu_id = "6666000103334211"
        request.org_req_date = "20230517"
        request.org_req_seq_id = "20230517111710E83514"
        request.org_hf_seq_id = "0036000topB230517111710P034c0a8304100000"
        request.receipt_data = getReceiptDataRucan()

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""