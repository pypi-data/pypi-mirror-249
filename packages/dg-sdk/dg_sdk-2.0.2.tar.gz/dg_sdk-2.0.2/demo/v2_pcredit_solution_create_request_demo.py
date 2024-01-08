import unittest
import dg_sdk
import json
from demo.demo_config import *


def getSubShopInfoList():
    dto = dict()
    # 二级商户号
    dto["sub_mer_id"] = "A4854135335181517376"
    # 二级商户名
    dto["sub_mer_name"] = "预二人"
    # 费率
    dto["fee_type"] = "02"
    # 店铺名称
    dto["mer_name"] = "盈盈超市"
    # 省份
    dto["province"] = "浙江省"
    # 市名
    dto["city"] = "杭州市"
    # 区、县
    dto["county"] = "西湖区"
    # 地址详情
    dto["detail"] = "古荡街道西溪路556号蚂蚁Z空间"

    dtoList = [dto]
    return json.dumps(dtoList)


def build_extend_infos():
    """
    非必填字段

    :return: 非必填字段组成的字典
    """
    extend_infos = dict()
    # 开发者的应用ID
    extend_infos["app_id"] = ""
    return extend_infos


class TestV2PcreditSolutionCreateRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 创建花呗分期方案 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2PcreditSolutionCreateRequest()
        request.req_seq_id = ""
        request.req_date = ""
        request.huifu_id = "6666000003084836"
        request.activity_name = "花呗分期商家贴息活动名称"
        request.start_time = "2019-07-08 00:00:00"
        request.end_time = "2039-07-10 00:00:00"
        request.min_money_limit = "1000"
        request.max_money_limit = "3000"
        request.amount_budget = "60000"
        request.install_num_str_list = "3"
        request.budget_warning_money = "58000"
        request.budget_warning_mail_list = "111@alipay.com"
        request.budget_warning_mobile_no_list = "13940001100"
        request.sub_shop_info_list = getSubShopInfoList()

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""