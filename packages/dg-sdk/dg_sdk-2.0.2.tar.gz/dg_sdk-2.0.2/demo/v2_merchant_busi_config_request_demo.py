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
    # 微信公众号APPID对应的秘钥
    extend_infos["wx_woa_secret"] = "64afb60bef3a22ac282aa7880cdaca98"
    # 微信小程序APPID对应的秘钥
    extend_infos["wx_applet_secret"] = "1323a4165a662d6e4f9f51b3f7a58e3f"
    # 渠道号
    extend_infos["bank_channel_no"] = "JQF00001"
    # 异步消息接收地址
    # extend_infos["async_return_url"] = ""
    return extend_infos


class TestV2MerchantBusiConfigRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 微信商户配置 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2MerchantBusiConfigRequest()
        request.req_seq_id = ""
        request.req_date = ""
        request.huifu_id = "6666000108854952"
        request.fee_type = "02"
        request.wx_woa_app_id = "wx3767c5bd01df5061"
        request.wx_woa_path = "https://paas.huifu.com/shouyin/demo/h5/"
        request.wx_applet_app_id = "wx8523175fea790f10"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""