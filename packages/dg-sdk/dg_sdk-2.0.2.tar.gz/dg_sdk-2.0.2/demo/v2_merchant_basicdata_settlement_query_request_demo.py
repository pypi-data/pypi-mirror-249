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
    # 结算方式
    extend_infos["settle_cycle"] = ""
    # 分页页码
    extend_infos["page_num"] = "1"
    # 交易状态
    extend_infos["trans_stat"] = "I"
    # 排序字段
    extend_infos["sort_column"] = "10"
    # 排序顺序
    extend_infos["sort_order"] = "DESC"
    return extend_infos


class TestV2MerchantBasicdataSettlementQueryRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 结算记录查询 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2MerchantBasicdataSettlementQueryRequest()
        request.req_seq_id = ""
        request.req_date = ""
        request.huifu_id = "6666000111938435"
        request.begin_date = "20200810"
        request.end_date = "20200810"
        request.page_size = "10"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""