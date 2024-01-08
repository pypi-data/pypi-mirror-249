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
    # 原请求流水号
    extend_infos["org_req_seq_id"] = "20230110155433defaultit655128593"
    # 原请求日期
    extend_infos["org_req_date"] = "20230110"
    # 原汇款订单号
    extend_infos["org_remittance_order_id"] = "20230110155433defaultit655128591"
    # 每页条数
    extend_infos["page_size"] = "1"
    # 分页页码
    extend_infos["page_no"] = "1"
    # 入账批次号
    # extend_infos["org_batch_no"] = ""
    return extend_infos


class TestV2TradeOnlinepaymentTransferRemittanceorderRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 汇付入账查询 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2TradeOnlinepaymentTransferRemittanceorderRequest()
        request.huifu_id = "6666000003100615"
        request.org_req_start_date = "20230110"
        request.org_req_end_date = "20230110"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""