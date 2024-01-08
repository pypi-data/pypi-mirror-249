import unittest
import dg_sdk
import json
from demo.demo_config import *


def getFileList():
    dto = dict()
    # 文件类型
    dto["file_type"] = "F50"
    # 文件jfileID
    dto["file_id"] = "b53e18b3-f933-357f-9a6f-952c6a021ba5"
    # 文件名称
    dto["file_name"] = "360huxi.jpg"

    dtoList = [dto]
    return json.dumps(dtoList)


def build_extend_infos():
    """
    非必填字段

    :return: 非必填字段组成的字典
    """
    extend_infos = dict()
    # 订单授权凭证
    extend_infos["order_ticket"] = "werwe234234234"
    # 签约且授权标识
    extend_infos["sign_and_auth"] = "Y"
    # 应用授权令牌
    extend_infos["app_auth_token"] = "test0004"
    # 营业执照编号
    extend_infos["license_code"] = ""
    # 营业执照有效期类型
    extend_infos["license_validity_type"] = "0"
    # 营业执照有效期开始日期
    extend_infos["license_begin_date"] = "20200429"
    # 营业执照有效期截止日期
    extend_infos["license_end_date"] = "29200429"
    return extend_infos


class TestV2MerchantDirectAlipayFacetofacesignApplyRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 支付宝直连-申请当面付代签约 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2MerchantDirectAlipayFacetofacesignApplyRequest()
        request.req_seq_id = ""
        request.req_date = ""
        request.huifu_id = "6666000003080750"
        request.upper_huifu_id = "6666000003078903"
        request.direct_category = "A_A01_4119"
        request.app_id = "AE150003019"
        request.contact_name = "hqqTEST"
        request.contact_mobile_no = "15800718101"
        request.contact_email = "24324@qq.com"
        request.account = "288000000345345"
        request.rate = "0.38"
        request.file_list = getFileList()

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""