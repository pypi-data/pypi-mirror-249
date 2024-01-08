import unittest
import dg_sdk
import json
from demo.demo_config import *


def getLocation():
    dto = dict()
    # 服务开始地点
    # dto["start_location"] = ""
    # 服务结束地点
    # dto["end_location"] = ""

    return json.dumps(dto)

def getTimeRange():
    dto = dict()
    # 服务开始时间
    # dto["start_time"] = ""
    # 服务结束时间
    # dto["end_time"] = ""
    # 服务开始时间备注
    # dto["start_time_remark"] = ""
    # 服务结束时间备注
    # dto["end_time_remark"] = ""

    return json.dumps(dto)

def getPostDiscounts():
    dto = dict()
    # 优惠名称
    # dto["name"] = ""
    # 优惠金额
    # dto["amount"] = ""
    # 优惠说明
    # dto["description"] = ""
    # 优惠数量
    # dto["count"] = ""

    dtoList = [dto]
    return json.dumps(dtoList)

def getPostPayments():
    dto = dict()
    # 付费名称
    # dto["name"] = ""
    # 付费金额
    # dto["amount"] = ""
    # 付费说明
    # dto["description"] = ""
    # 付费数量
    # dto["count"] = ""

    dtoList = [dto]
    return json.dumps(dtoList)


def build_extend_infos():
    """
    非必填字段

    :return: 非必填字段组成的字典
    """
    extend_infos = dict()
    # 创建服务订单返回的汇付全局流水号
    # extend_infos["org_hf_seq_id"] = ""
    # 服务订单创建请求流水号
    # extend_infos["org_req_seq_id"] = ""
    # 后付费项目
    # extend_infos["post_payments"] = getPostPayments()
    # 商户优惠
    # extend_infos["post_discounts"] = getPostDiscounts()
    # 服务位置
    # extend_infos["location"] = getLocation()
    # 完结服务时间
    # extend_infos["complete_time"] = ""
    return extend_infos


class TestV2TradePayscoreServiceorderCompleteRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 完结支付分订单 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2TradePayscoreServiceorderCompleteRequest()
        request.huifu_id = "6666000108854952"
        request.out_order_no = "test"
        request.ord_amt = "test"
        request.time_range = getTimeRange()

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""