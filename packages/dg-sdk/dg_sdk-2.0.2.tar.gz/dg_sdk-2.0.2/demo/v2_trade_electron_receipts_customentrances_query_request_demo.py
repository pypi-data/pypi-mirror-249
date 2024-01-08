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
    # 品牌ID
    dto["brand_id"] = "11"

    return dto;


def build_extend_infos():
    """
    非必填字段

    :return: 非必填字段组成的字典
    """
    extend_infos = dict()
    # 票据信息
    extend_infos["receipt_data"] = getReceiptDataRucan()
    return extend_infos


class TestV2TradeElectronReceiptsCustomentrancesQueryRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 查询小票自定义入口 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2TradeElectronReceiptsCustomentrancesQueryRequest()
        request.req_seq_id = ""
        request.req_date = ""
        request.huifu_id = "6666000103334211"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""