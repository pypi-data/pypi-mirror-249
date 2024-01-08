import unittest
import dg_sdk
import json
from demo.demo_config import *


def getFileInfo():
    dto = dict()
    # 回复图片1
    # dto["response_pic1"] = ""
    # 回复图片2
    # dto["response_pic2"] = ""
    # 回复图片3
    # dto["response_pic3"] = ""
    # 回复图片4
    # dto["response_pic4"] = ""

    return json.dumps(dto)


def build_extend_infos():
    """
    非必填字段

    :return: 非必填字段组成的字典
    """
    extend_infos = dict()
    # 文件列表
    # extend_infos["file_info"] = getFileInfo()
    return extend_infos


class TestV2MerchantComplaintReplyRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 回复用户 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2MerchantComplaintReplyRequest()
        request.req_seq_id = ""
        request.req_date = ""
        request.complaint_id = "200000020221020220032603511"
        request.complainted_mchid = "535295270"
        request.response_content = "该问题请联系商家处理，谢谢。"
        request.jump_url = ""
        request.jump_url_text = ""
        request.mch_id = "1502073961"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""