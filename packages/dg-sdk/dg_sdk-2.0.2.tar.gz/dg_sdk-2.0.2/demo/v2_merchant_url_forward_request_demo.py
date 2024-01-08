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
    # 手机号
    extend_infos["phone"] = "13917352618"
    # 跳转地址失效时间
    extend_infos["expires"] = "50000"
    # 返回页面URL
    # extend_infos["back_page_url"] = ""
    # 异步接收URL
    # extend_infos["async_receive_url"] = ""
    return extend_infos


class TestV2MerchantUrlForwardRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 商户统一进件（页面版） - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2MerchantUrlForwardRequest()
        request.req_seq_id = ""
        request.req_date = ""
        request.upper_huifu_id = "6666000123123123"
        request.store_id = "test"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""