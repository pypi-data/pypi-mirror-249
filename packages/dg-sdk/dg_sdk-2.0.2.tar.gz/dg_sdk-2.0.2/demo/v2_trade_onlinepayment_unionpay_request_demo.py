import unittest
import dg_sdk
import json
from demo.demo_config import *


def getRiskCheckData():
    dto = dict()
    # 基站地址
    dto["base_station"] = "7"
    # ip地址
    # dto["ip_addr"] = ""
    # 纬度
    dto["latitude"] = "4"
    # 经度
    dto["longitude"] = "3"

    return json.dumps(dto)

def getAcctSplitBunchRucan():
    dto = dict()
    # 分账明细
    # dto["acct_infos"] = getAcctInfos()

    return json.dumps(dto)

def getAcctInfos():
    dto = dict()
    # 分账金额
    # dto["div_amt"] = ""
    # 商户号
    # dto["huifu_id"] = ""
    # 账户号
    # dto["acct_id"] = ""

    dtoList = [dto]
    return dtoList


def build_extend_infos():
    """
    非必填字段

    :return: 非必填字段组成的字典
    """
    extend_infos = dict()
    # 卡号锁定标识
    extend_infos["card_number_lock"] = ""
    # 直通模式的银行标识
    extend_infos["ebank_en_abbr"] = ""
    # 交易银行卡卡号
    extend_infos["pay_card_no"] = ""
    # 支付卡类型
    extend_infos["pay_card_type"] = "04"
    # 订单失效时间
    extend_infos["time_expire"] = ""
    # 分账对象
    # extend_infos["acct_split_bunch"] = getAcctSplitBunchRucan()
    # 前端跳转地址
    extend_infos["front_url"] = "https://www.service.com/getresp"
    # 异步通知地址
    extend_infos["notify_url"] = "https://www.service.com/getresp"
    # 备注
    extend_infos["remark"] = "merPriv11"
    return extend_infos


class TestV2TradeOnlinepaymentUnionpayRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 银联统一在线收银台接口 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2TradeOnlinepaymentUnionpayRequest()
        request.huifu_id = "6666000108854952"
        request.req_date = ""
        request.req_seq_id = ""
        request.trans_amt = "0.11"
        request.order_desc = "通用性商品1"
        request.risk_check_data = getRiskCheckData()

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""