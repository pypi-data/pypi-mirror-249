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
    # 分页开始位置
    extend_infos["offset"] = "1"
    # 分页大小
    extend_infos["limit"] = "5"
    # 通道风险类型
    extend_infos["risk_type"] = ""
    # 汇付商户号
    extend_infos["huifu_id"] = ""
    # 支付宝推送流水号
    extend_infos["risk_biz_id"] = ""
    # 是否可申诉
    extend_infos["support_appeal"] = ""
    return extend_infos


class TestV2MerchantComplaintAliRiskinfoQueryRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 支付宝投诉查询 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2MerchantComplaintAliRiskinfoQueryRequest()
        request.req_seq_id = ""
        request.req_date = ""
        request.begin_date = "20221115"
        request.end_date = "20221115"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""