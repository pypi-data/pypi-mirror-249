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
    # 结算信息配置
    # extend_infos["&lt;span class&#x3D;&quot;extend settle_config&quot;&gt;settle_config&lt;/span&gt;"] = ""
    # 结算卡信息
    # extend_infos["&lt;span class&#x3D;&quot;extend card_info&quot;&gt;card_info&lt;/span&gt;"] = ""
    # 取现配置列表
    # extend_infos["&lt;span class&#x3D;&quot;extend cash_config&quot;&gt;cash_config&lt;/span&gt;"] = ""
    # 文件列表
    # extend_infos["&lt;span class&#x3D;&quot;extend file_list&quot;&gt;file_list&lt;/span&gt;"] = ""
    # 延迟入账开关
    # extend_infos["delay_flag"] = ""
    return extend_infos


class TestV2UserBusiOpenRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 用户业务入驻 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2UserBusiOpenRequest()
        request.huifu_id = "6666000105765113"
        request.req_seq_id = ""
        request.req_date = ""
        request.upper_huifu_id = "6666000003084836"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""