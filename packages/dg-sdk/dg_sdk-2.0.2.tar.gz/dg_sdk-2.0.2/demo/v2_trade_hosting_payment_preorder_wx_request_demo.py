import unittest
import dg_sdk
import json
from demo.demo_config import *


def getBizInfo():
    dto = dict()
    # 付款人验证（微信）
    # dto["payer_check_wx"] = getPayCheckWx()
    # 个人付款人信息
    # dto["person_payer"] = getPersonPayer()

    return json.dumps(dto)

def getPersonPayer():
    dto = dict()
    # 姓名
    # dto["name"] = ""
    # 证件类型
    # dto["cert_type"] = ""
    # 证件号
    # dto["cert_no"] = ""

    return dto;

def getPayCheckWx():
    dto = dict()
    # 指定支付者
    # dto["limit_payer"] = ""
    # 微信实名验证
    # dto["real_name_flag"] = ""

    return dto;

def getMiniappDataRucan():
    dto = dict()
    # 是否生成scheme_code
    dto["need_scheme"] = "Y"
    # 应用ID
    dto["seq_id"] = "APP_2022033147154783"
    # 私有信息
    dto["private_info"] = "oppsHosting://"

    return json.dumps(dto)

def getAcctSplitBunchRucan():
    dto = dict()
    # 分账明细
    dto["acct_infos"] = getAcctInfosRucan()

    return json.dumps(dto)

def getAcctInfosRucan():
    dto = dict()
    # 分账金额
    dto["div_amt"] = "0.01"
    # 被分账方ID
    dto["huifu_id"] = "6666000003100616"

    dtoList = [dto]
    return dtoList


def build_extend_infos():
    """
    非必填字段

    :return: 非必填字段组成的字典
    """
    extend_infos = dict()
    # 收银台ID
    extend_infos["checkout_id"] = ""
    # 是否延迟交易
    extend_infos["delay_acct_flag"] = "Y"
    # 分账对象
    extend_infos["acct_split_bunch"] = getAcctSplitBunchRucan()
    # 交易失效时间
    extend_infos["time_expire"] = "20231127233423"
    # 业务信息
    # extend_infos["biz_info"] = getBizInfo()
    # 交易异步通知地址
    extend_infos["notify_url"] = "https://callback.service.com/xx"
    return extend_infos


class TestV2TradeHostingPaymentPreorderWxRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 微信小程序预下单接口 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2TradeHostingPaymentPreorderWxRequest()
        request.pre_order_type = "3"
        request.req_date = ""
        request.req_seq_id = ""
        request.huifu_id = "6666000003100616"
        request.trans_amt = "0.13"
        request.goods_desc = "app跳微信消费"
        request.miniapp_data = getMiniappDataRucan()

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""