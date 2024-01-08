import unittest
import dg_sdk
import json
from demo.demo_config import *


def getBizInfo():
    dto = dict()
    # 付款人验证（支付宝）
    # dto["payer_check_ali"] = getPayerCheckAli()
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
    # 手机号
    # dto["mobile"] = ""

    return dto;

def getPayerCheckAli():
    dto = dict()
    # 是否提供校验身份信息
    # dto["need_check_info"] = ""
    # 允许的最小买家年龄
    # dto["min_age"] = ""
    # 是否强制校验付款人身份信息
    # dto["fix_buyer"] = ""

    return dto;

def getAppData():
    dto = dict()
    # 小程序返回码
    dto["app_schema"] = "app跳转链接"
    # 私有信息
    # dto["private_info"] = ""

    return json.dumps(dto)

def getAcctSplitBunchRucan():
    dto = dict()
    # 分账明细
    dto["acct_infos"] = getAcctInfosRucan()

    return json.dumps(dto)

def getAcctInfosRucan():
    dto = dict()
    # 分账金额
    dto["div_amt"] = "0.08"
    # 被分账方ID
    dto["huifu_id"] = "6666000111546360"

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
    extend_infos["delay_acct_flag"] = "N"
    # 分账对象
    extend_infos["acct_split_bunch"] = getAcctSplitBunchRucan()
    # 交易失效时间
    # extend_infos["time_expire"] = ""
    # 业务信息
    # extend_infos["biz_info"] = getBizInfo()
    # 异步通知地址
    extend_infos["notify_url"] = "https://callback.service.com/xx"
    return extend_infos


class TestV2TradeHostingPaymentPreorderAliRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 支付宝小程序预下单接口 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2TradeHostingPaymentPreorderAliRequest()
        request.huifu_id = "6666000111546360"
        request.req_date = ""
        request.req_seq_id = ""
        request.pre_order_type = "2"
        request.trans_amt = "0.10"
        request.goods_desc = "app跳支付宝消费"
        request.app_data = getAppData()

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""