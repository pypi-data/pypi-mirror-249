import unittest
import dg_sdk
import json
from demo.demo_config import *


def getAcctSplitBunchList():
    dto = dict()
    # 分账比例
    dto["fee_rate"] = "100"
    # 汇付Id
    dto["huifu_id"] = "6666000105582434"

    dtoList = [dto]
    return json.dumps(dtoList)


def build_extend_infos():
    """
    非必填字段

    :return: 非必填字段组成的字典
    """
    extend_infos = dict()
    # 分账明细
    extend_infos["acct_split_bunch_list"] = getAcctSplitBunchList()
    # 分账手续费外扣开关
    extend_infos["out_fee_flag"] = "1"
    # 分账手续费外扣时的账户类型
    extend_infos["out_fee_acct_type"] = "01"
    # 分账手续费外扣汇付ID
    extend_infos["out_fee_huifuid"] = "6666000105582434"
    # 固定手续费
    extend_infos["split_fee_rate"] = "10.89"
    # 百分比手续费
    extend_infos["per_amt"] = "99"
    # 异步地址
    extend_infos["async_return_url"] = "http://192.168.85.157:30031/sspm/testVirgo"
    return extend_infos


class TestV2MerchantSplitConfigRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 商户分账配置(2022) - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2MerchantSplitConfigRequest()
        request.req_seq_id = ""
        request.req_date = ""
        request.huifu_id = "6666000105582434"
        request.rule_origin = "02"
        request.div_flag = "Y"
        request.apply_ratio = "100"
        request.start_type = "0"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""