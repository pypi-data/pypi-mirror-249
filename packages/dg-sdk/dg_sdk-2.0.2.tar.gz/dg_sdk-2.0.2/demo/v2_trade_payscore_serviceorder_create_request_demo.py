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

def getRiskFund():
    dto = dict()
    # 风险名称
    # dto["name"] = ""
    # 风险金额
    # dto["amount"] = ""
    # 风险说明
    # dto["description"] = ""

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
    # 服务ID
    # extend_infos["service_id"] = ""
    # 子商户公众号ID
    # extend_infos["sub_appid"] = ""
    # 场景类型
    # extend_infos["trade_scene"] = ""
    # 费率类型
    # extend_infos["pay_scene"] = ""
    # 从业机构公众号下的用户标识
    # extend_infos["openid"] = ""
    # 子商户公众号下的用户标识
    # extend_infos["sub_openid"] = ""
    # 后付费项目
    # extend_infos["post_payments"] = getPostPayments()
    # 商户优惠
    # extend_infos["post_discounts"] = getPostDiscounts()
    # 服务位置
    # extend_infos["location"] = getLocation()
    # 附加数据
    # extend_infos["attach"] = ""
    return extend_infos


class TestV2TradePayscoreServiceorderCreateRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 创建支付分订单 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2TradePayscoreServiceorderCreateRequest()
        request.req_date = ""
        request.req_seq_id = ""
        request.huifu_id = "6666000108854952"
        request.service_introduction = "test"
        request.risk_fund = getRiskFund()
        request.time_range = getTimeRange()
        request.notify_url = "test"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""