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
    # 商户与商家的联系渠道
    dto["merchant_contact_information"] = getMerchantContactInformation()

    return dto;

def getMerchantContactInformation():
    dto = dict()
    # 商户售后咨询电话
    # dto["consultation_phone_number"] = ""

    return dto;


def build_extend_infos():
    """
    非必填字段

    :return: 非必填字段组成的字典
    """
    extend_infos = dict()
    return extend_infos


class TestV2TradeElectronReceiptsUploadRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 上传电子小票图片 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2TradeElectronReceiptsUploadRequest()
        request.req_seq_id = ""
        request.req_date = ""
        request.huifu_id = "6666000103334211"
        request.org_req_date = "20230517"
        request.org_req_seq_id = "20230517111710E83514"
        request.org_hf_seq_id = "0036000topB230517111710P034c0a8304100000"
        request.receipt_data = getReceiptDataRucan()
        request.file_name = "电子小票1.jpg"
        request.image_content = "/9j/4AAQSkZJRgABAQAASABIAUAf//Z……"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""