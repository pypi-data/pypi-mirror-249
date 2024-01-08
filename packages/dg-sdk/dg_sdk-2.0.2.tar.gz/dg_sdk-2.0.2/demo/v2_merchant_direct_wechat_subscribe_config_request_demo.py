import unittest
import dg_sdk
import json
from demo.demo_config import *


def getPayPathConfList():
    dto = dict()
    # 授权目录
    dto["jsapi_path"] = "http://www.dsf.com/init"

    dtoList = [dto]
    return json.dumps(dtoList)

def getSubscribeConfList():
    dto = dict()
    # 关联APPID
    dto["sub_appid"] = "wx5934540532"
    # 推荐关注APPID服务商的公众号APPID；与receipt_appid二选一；&lt;font color&#x3D;&quot;green&quot;&gt;示例值：wx5934540532&lt;/font&gt;
    dto["subscribe_appid"] = "oQOa46X2FxRqEy6F4YmwIRCrA7Mk"
    # 支付凭证推荐小程序appid需为通过微信认证的小程序appid，且认证主体与服务商主体一致；与subscribe_appid二选一；&lt;font color&#x3D;&quot;green&quot;&gt;示例值：wx852a790f100000fe&lt;/font&gt;
    dto["receipt_appid"] = "wx852a790f100000fe"

    dtoList = [dto]
    return json.dumps(dtoList)

def getBindAppIdConfList():
    dto = dict()
    # 关联APPID
    dto["sub_appid"] = "oQOa46X2FxRqEy6F4YmwIRCrA7Mk"

    dtoList = [dto]
    return json.dumps(dtoList)


def build_extend_infos():
    """
    非必填字段

    :return: 非必填字段组成的字典
    """
    extend_infos = dict()
    # 绑定APPID配置
    extend_infos["bind_app_id_conf_list"] = getBindAppIdConfList()
    # 关注配置
    extend_infos["subscribe_conf_list"] = getSubscribeConfList()
    # 支付目录配置
    extend_infos["pay_path_conf_list"] = getPayPathConfList()
    return extend_infos


class TestV2MerchantDirectWechatSubscribeConfigRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 微信直连-微信关注配置 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2MerchantDirectWechatSubscribeConfigRequest()
        request.req_seq_id = ""
        request.req_date = ""
        request.huifu_id = "6666000003099420"
        request.app_id = "wx3767c5bd01df5061"
        request.mch_id = "1552470931"
        request.sub_mchid = "10888880"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""