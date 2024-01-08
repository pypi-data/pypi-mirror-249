import unittest
import dg_sdk
import json
from demo.demo_config import *


def getRiskCheckData():
    dto = dict()
    # ip地址
    # dto["ip_addr"] = ""
    # 基站地址
    dto["base_station"] = "3"
    # 纬度
    dto["latitude"] = "2"
    # 经度
    dto["longitude"] = "1"
    # 产品子类
    # dto["sub_product"] = ""
    # 转账原因
    # dto["transfer_type"] = ""

    return json.dumps(dto)

def getAcctSplitBunch():
    dto = dict()
    # 分账明细
    dto["acct_infos"] = getAcctInfosRucan()

    return json.dumps(dto)

def getAcctInfosRucan():
    dto = dict()
    # 分账金额
    dto["div_amt"] = "0.01"
    # 被分账方ID
    dto["huifu_id"] = "6666000103423237"
    # 被分账方账户号
    dto["acct_id"] = "C01400109"

    dtoList = [dto]
    return dtoList


def build_extend_infos():
    """
    非必填字段

    :return: 非必填字段组成的字典
    """
    extend_infos = dict()
    # 原交易请求日期
    extend_infos["org_req_date"] = "20221108"
    # 原交易请求流水号
    extend_infos["org_req_seq_id"] = "2022072724398620211667900766"
    # 原交易全局流水号
    extend_infos["org_hf_seq_id"] = ""
    # 分账对象
    extend_infos["acct_split_bunch"] = getAcctSplitBunch()
    # 安全信息
    extend_infos["risk_check_data"] = getRiskCheckData()
    # 交易类型
    # extend_infos["pay_type"] = ""
    # 备注
    extend_infos["remark"] = "remark123"
    # 原交易商户订单号
    # extend_infos["org_mer_ord_id"] = ""
    return extend_infos


class TestV2TradePaymentDelaytransConfirmRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 交易确认接口 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2TradePaymentDelaytransConfirmRequest()
        request.req_date = ""
        request.req_seq_id = ""
        request.huifu_id = "6666000103423237"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""