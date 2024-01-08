import unittest
import dg_sdk
import json
from demo.demo_config import *


def getRiskCheckData():
    dto = dict()
    # 转账原因
    dto["transfer_type"] = "04"
    # 产品子类
    dto["sub_product"] = "1"
    # 纬度
    # dto["latitude"] = ""
    # 经度
    # dto["longitude"] = ""
    # 基站地址
    # dto["base_station"] = ""
    # IP地址
    # dto["ip_addr"] = ""

    return json.dumps(dto)

def getAcctSplitBunch():
    dto = dict()
    # 分账明细
    dto["acct_infos"] = getAcctInfos()

    return json.dumps(dto)

def getAcctInfos():
    dto = dict()
    # 分账金额
    dto["div_amt"] = "0.01"
    # 被分账方ID
    dto["huifu_id"] = "6666000018344461"
    # 被分账方账户号
    # dto["acct_id"] = ""

    dtoList = [dto]
    return dtoList


def build_extend_infos():
    """
    非必填字段

    :return: 非必填字段组成的字典
    """
    extend_infos = dict()
    # ~~发起方商户号~~
    # extend_infos["~~huifu_id~~"] = ""
    # 商品描述
    # extend_infos["good_desc"] = ""
    # 备注
    # extend_infos["remark"] = ""
    # 是否延迟交易
    # extend_infos["delay_acct_flag"] = ""
    # 出款方账户号
    # extend_infos["out_acct_id"] = ""
    return extend_infos


class TestV2TradeAcctpaymentPayRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 余额支付 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2TradeAcctpaymentPayRequest()
        request.req_seq_id = ""
        request.req_date = ""
        request.out_huifu_id = "6666000018344461"
        request.ord_amt = "0.01"
        request.acct_split_bunch = getAcctSplitBunch()
        request.risk_check_data = getRiskCheckData()

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""