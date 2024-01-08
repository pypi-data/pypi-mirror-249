import unittest
import dg_sdk
import json
from demo.demo_config import *


def getZftSplitReceiverList():
    dto = dict()
    # 分账接收方方类型
    dto["split_type"] = "loginName"
    # 分账接收方账号
    dto["account"] = "739100190@qq.com"
    # 分账接收方真实姓名新增分账关系时必填。解绑分账关系时非必填；&lt;font color&#x3D;&quot;green&quot;&gt;示例值：张三&lt;/font&gt;
    dto["name"] = "邵文"
    # 分账关系描述
    dto["memo"] = "M20220820032239499098320"

    dtoList = [dto]
    return json.dumps(dtoList)


def build_extend_infos():
    """
    非必填字段

    :return: 非必填字段组成的字典
    """
    extend_infos = dict()
    return extend_infos


class TestV2MerchantDirectZftReceiverConfigRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 直付通分账关系绑定解绑 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2MerchantDirectZftReceiverConfigRequest()
        request.req_seq_id = ""
        request.req_date = ""
        request.huifu_id = "6666000103886183"
        request.app_id = "2021002171607880"
        request.split_flag = "1"
        request.zft_split_receiver_list = getZftSplitReceiverList()
        request.status = "0"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""