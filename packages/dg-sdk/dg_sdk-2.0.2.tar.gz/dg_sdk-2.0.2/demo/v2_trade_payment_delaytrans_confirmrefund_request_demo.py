import unittest
import dg_sdk
import json
from demo.demo_config import *


def getAcctSplitBunch():
    dto = dict()
    # 分账明细
    dto["acct_infos"] = getAcctInfos()

    return json.dumps(dto)

def getAcctInfos():
    dto = dict()
    # 被分账方ID
    dto["huifu_id"] = "6666000003109208"
    # 分账金额(元)
    dto["div_amt"] = "0.01"
    # 垫资金额(元)
    # dto["part_loan_amt"] = ""

    dtoList = [dto]
    return dtoList


def build_extend_infos():
    """
    非必填字段

    :return: 非必填字段组成的字典
    """
    extend_infos = dict()
    # 分账对象
    extend_infos["acct_split_bunch"] = getAcctSplitBunch()
    # 是否垫资退款
    # extend_infos["loan_flag"] = ""
    # 垫资承担者
    # extend_infos["loan_undertaker"] = ""
    # 垫资账户类型
    # extend_infos["loan_acct_type"] = ""
    return extend_infos


class TestV2TradePaymentDelaytransConfirmrefundRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 交易确认退款接口 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2TradePaymentDelaytransConfirmrefundRequest()
        request.req_date = ""
        request.req_seq_id = ""
        request.huifu_id = "6666000103423237"
        request.org_req_date = "20221108"
        request.org_req_seq_id = "20221108349713659620211667908395"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""