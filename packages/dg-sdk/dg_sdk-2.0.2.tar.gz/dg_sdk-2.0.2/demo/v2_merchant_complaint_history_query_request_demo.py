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
    extend_infos["offset"] = "10"
    # 分页大小
    extend_infos["limit"] = "1"
    return extend_infos


class TestV2MerchantComplaintHistoryQueryRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 查询投诉协商历史 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2MerchantComplaintHistoryQueryRequest()
        request.req_seq_id = ""
        request.req_date = ""
        request.complaint_id = "200000020221019110032287912"
        request.mch_id = "1507920721"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""