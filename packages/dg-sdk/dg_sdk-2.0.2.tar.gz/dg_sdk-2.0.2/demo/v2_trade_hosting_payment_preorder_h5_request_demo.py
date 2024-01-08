import unittest
import dg_sdk
import json
from demo.demo_config import *


def getBizInfo():
    dto = dict()
    # 付款人验证（支付宝）
    dto["payer_check_ali"] = getPayerCheckAli()
    # 付款人验证（微信）
    dto["payer_check_wx"] = getPayerCheckWx()
    # 个人付款人信息
    dto["person_payer"] = getPersonPayer()

    return json.dumps(dto)

def getPersonPayer():
    dto = dict()
    # 姓名
    dto["name"] = "张三"
    # 证件类型
    dto["cert_type"] = "IDENTITY_CARD"
    # 证件号
    dto["cert_no"] = "Mc5pjf+b/Keyi/t/wnHJtJYPHd1xXntq6tau0j8SjLzJx+q2xL2mOmKRDAYHu4uY1JSoPbWBhq9b7gT7Kxb1CYnkj7vmSlTYl8tVKfOPFyauOE66ew9cmkhmUzjzVTM1quoR63pP8+ESvZZrRPFE4YY9PXO9It9JINo8bjX22fQEFZKmXaEcqnSDcl2LUuJguvQ0LejI6zbxCJhfSHbz7HhHTIZTUchkWpKoy8YlfG27FumjXHU3rIjbrgmc+8pXbyndTNlui1+lTu6deibGKq/CpShA8z5FkHsn6/1O9ZEjLcnPnSLUwCnu75UlVVk66g+hR1OGdRrFMfYQnK7Lzw=="
    # 手机号
    dto["mobile"] = "15012345678"

    return dto;

def getPayerCheckWx():
    dto = dict()
    # 指定支付者
    dto["limit_payer"] = "ADULT"
    # 微信实名验证
    dto["real_name_flag"] = "Y"

    return dto;

def getPayerCheckAli():
    dto = dict()
    # 是否提供校验身份信息
    dto["need_check_info"] = "T"
    # 允许的最小买家年龄
    dto["min_age"] = "12"
    # 是否强制校验付款人身份信息
    dto["fix_buyer"] = "F"

    return dto;

def getHostingData():
    dto = dict()
    # 项目标题
    dto["project_title"] = "收银台标题"
    # 半支付托管项目号
    dto["project_id"] = "PROJECTID2022032912492559"
    # 商户私有信息
    dto["private_info"] = "商户私有信息test"
    # 回调地址
    dto["callback_url"] = "https://paas.huifu.com"

    return json.dumps(dto)

def getAcctSplitBunch():
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
    extend_infos["acct_split_bunch"] = getAcctSplitBunch()
    # 交易失效时间
    # extend_infos["time_expire"] = ""
    # 业务信息
    extend_infos["biz_info"] = getBizInfo()
    # 交易异步通知地址
    extend_infos["notify_url"] = "https://callback.service.com/xx"
    return extend_infos


class TestV2TradeHostingPaymentPreorderH5RequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # H5、PC预下单接口 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2TradeHostingPaymentPreorderH5Request()
        request.req_date = ""
        request.req_seq_id = ""
        request.huifu_id = "6666000111546360"
        request.trans_amt = "0.10"
        request.goods_desc = "支付托管消费"
        request.pre_order_type = "1"
        request.hosting_data = getHostingData()

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""