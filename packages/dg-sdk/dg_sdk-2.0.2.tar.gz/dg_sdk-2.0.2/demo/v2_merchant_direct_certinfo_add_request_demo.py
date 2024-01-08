import unittest
import dg_sdk
import json
from demo.demo_config import *


def getFileList():
    dto = dict()
    # 文件类型
    dto["file_type"] = "F53"
    # 文件jfileID
    dto["file_id"] = "9aec5b9e-816f-3ebf-8fe8-4146348ce2b0"
    # 文件名称
    dto["file_name"] = "证书1202208189390.crt"

    dtoList = [dto]
    return json.dumps(dtoList)


def build_extend_infos():
    """
    非必填字段

    :return: 非必填字段组成的字典
    """
    extend_infos = dict()
    # 商户号
    extend_infos["mch_id"] = "360634064"
    # 证书序列号
    extend_infos["cert_sn"] = "20220818883326714"
    # 服务商密钥
    extend_infos["secret_key"] = "RERE202208182319"
    # 证书类型标记
    extend_infos["cert_flag"] = ""
    return extend_infos


class TestV2MerchantDirectCertinfoAddRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 证书登记 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2MerchantDirectCertinfoAddRequest()
        request.req_seq_id = ""
        request.req_date = ""
        request.upper_huifu_id = "6666000103509367"
        request.pay_way = "W"
        request.app_id = "20220818198665087"
        request.file_list = getFileList()

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""