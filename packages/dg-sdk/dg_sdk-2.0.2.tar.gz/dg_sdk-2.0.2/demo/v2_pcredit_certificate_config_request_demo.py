import unittest
import dg_sdk
import json
from demo.demo_config import *


def getFileList():
    dto = dict()
    # 文件类型
    dto["file_type"] = "F120"
    # 文件jfileID
    dto["file_id"] = "57cc7f00-600a-33ab-b614-6221bbf2e529"
    # 文件名称
    dto["file_name"] = "test420.jpg"

    dtoList = [dto]
    return json.dumps(dtoList)


def build_extend_infos():
    """
    非必填字段

    :return: 非必填字段组成的字典
    """
    extend_infos = dict()
    return extend_infos


class TestV2PcreditCertificateConfigRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 分期证书配置 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2PcreditCertificateConfigRequest()
        request.req_seq_id = ""
        request.req_date = ""
        request.app_id = "2019090666961966"
        request.file_list = getFileList()

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""