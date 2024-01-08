import unittest
import dg_sdk
import json
from demo.demo_config import *


def getRelieveCertDataList():
    dto = dict()
    # 凭证的唯一ID
    dto["request_id"] = "1efc8c73afd64fc1b1fc50a834a54be0"
    # 凭证类型
    dto["type"] = "IMAGE"
    # 凭证code
    dto["code"] = "904"
    # 凭证的内容
    dto["info_data"] = "edd2d893-d3c2-342b-9ded-993913effce9"

    dtoList = [dto]
    return json.dumps(dtoList)


def build_extend_infos():
    """
    非必填字段

    :return: 非必填字段组成的字典
    """
    extend_infos = dict()
    return extend_infos


class TestV2MerchantComplaintSubmitCertificatesRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 支付宝申诉提交凭证 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2MerchantComplaintSubmitCertificatesRequest()
        request.req_seq_id = ""
        request.req_date = ""
        request.risk_biz_id = "b1e11c97badf1ba025399ee0332d8fb1-ISV"
        request.relieving_id = "653739ab36362810b7203b304d6f3883"
        request.relieve_risk_type = "SMID_MERCHANT"
        request.relieve_cert_data_list = getRelieveCertDataList()

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""