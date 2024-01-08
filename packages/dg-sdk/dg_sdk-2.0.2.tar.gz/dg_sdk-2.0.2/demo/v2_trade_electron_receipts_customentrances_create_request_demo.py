import unittest
import dg_sdk
import json
from demo.demo_config import *


def getReceiptData():
    dto = dict()
    # 三方通道类型
    dto["third_channel_type"] = "T"
    # 微信票据信息
    dto["wx_receipt_data"] = getWxReceiptData()

    return json.dumps(dto)

def getWxReceiptData():
    dto = dict()
    # 品牌ID
    dto["brand_id"] = "1"
    # 自定义入口种类
    dto["custom_entrance_type"] = "MERCHANT_ACTIVITY"
    # 副标题
    dto["sub_title"] = "1"
    # 商品缩略图URL
    dto["goods_thumbnail_url"] = "1"
    # 入口展示开始时间
    dto["start_time"] = "2023-08-17T13:20:00+08:00"
    # 入口展示结束时间
    dto["end_time"] = "2023-08-18T11:20:00+08:00"
    # 自定义入口状态
    dto["custom_entrance_state"] = "ONLINE"
    # 请求业务单据号
    dto["out_request_no"] = "1"
    # 跳转信息
    dto["jump_link_data"] = getJumpLinkData()

    return dto;

def getJumpLinkData():
    dto = dict()
    # 商家小程序AppID
    dto["mini_programs_app_id"] = "oBmItsxLKa6pd5dSHK4xRLXTt05M"
    # 商家小程序path
    dto["mini_programs_path"] = "https://wxpaylogo.qpic.cn/wxpaylogo/PiajxSqBRaEIPAeia7ImvtsoMpdQ8uEd23s8VtfKDXa04FZk8kXDeH9Q/0"

    return dto;


def build_extend_infos():
    """
    非必填字段

    :return: 非必填字段组成的字典
    """
    extend_infos = dict()
    # 票据信息
    extend_infos["receipt_data"] = getReceiptData()
    return extend_infos


class TestV2TradeElectronReceiptsCustomentrancesCreateRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 创建修改小票自定义入口 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2TradeElectronReceiptsCustomentrancesCreateRequest()
        request.req_seq_id = ""
        request.req_date = ""
        request.huifu_id = "6666000103334211"
        request.operate_type = "A"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""