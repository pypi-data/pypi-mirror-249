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


class TestV2MerchantComplaintDownloadPictureRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 投诉图片下载 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2MerchantComplaintDownloadPictureRequest()
        request.req_seq_id = ""
        request.req_date = ""
        request.media_url = "https://api.mch.weixin.qq.com/v3/merchant-service/images/ChsyMDAwMDAwMjAyMjEwMTkyMjAwMzI0MjEzODUYACCN78OaBigBMAE4AQ%3D%3D"
        request.complaint_id = "test"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""