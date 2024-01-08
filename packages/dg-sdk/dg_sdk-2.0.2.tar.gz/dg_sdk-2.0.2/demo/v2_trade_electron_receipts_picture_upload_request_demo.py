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
    return extend_infos


class TestV2TradeElectronReceiptsPictureUploadRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 图片上传 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2TradeElectronReceiptsPictureUploadRequest()
        request.req_seq_id = ""
        request.req_date = ""
        request.huifu_id = "6666000103334211"
        request.third_channel_type = "T"
        request.file_name = "1电子小票1.jpg"
        request.image_content = "/9j/4AAQSkZJRgABAQAASABIAAD/4QBYRXhpZgC……"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""