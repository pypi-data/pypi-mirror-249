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
    extend_infos["offset"] = ""
    # 分页大小
    extend_infos["limit"] = ""
    # 被诉的汇付商户ID
    extend_infos["huifu_id"] = ""
    # 被诉的商户名称
    extend_infos["reg_name"] = ""
    # 微信订单号
    extend_infos["transaction_id"] = ""
    # 微信投诉单号
    extend_infos["complaint_id"] = ""
    # 投诉状态
    extend_infos["complaint_state"] = ""
    # 用户投诉次数
    extend_infos["user_complaint_times"] = ""
    # 是否有待回复的用户留言
    extend_infos["incoming_user_response"] = "0"
    return extend_infos


class TestV2MerchantComplaintListInfoQueryRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 查询投诉单列表及详情 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2MerchantComplaintListInfoQueryRequest()
        request.req_seq_id = ""
        request.req_date = ""
        request.begin_date = "2022-10-20"
        request.end_date = "2022-10-20"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""