import unittest
import dg_sdk
import json
from demo.demo_config import *



def build_extend_infos():
    """
    非必填字段

    :return: 非必填字段组成的字典
    """
    extend_infos = dict()
    # 开户银行全称（含支行）
    extend_infos["bank_name"] = "中国农业银行股份有限公司上海马当路支行"
    # 开户银行联行号
    extend_infos["bank_branch_id"] = "103290040169"
    return extend_infos


class TestV2MerchantDirectWechatSettlementinfoModifyRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 微信直连-修改微信结算帐号 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2MerchantDirectWechatSettlementinfoModifyRequest()
        request.req_seq_id = ""
        request.req_date = ""
        request.huifu_id = "6666000003098550"
        request.app_id = "wxd2da4051c9e32b86"
        request.mch_id = "1552470931"
        request.sub_mchid = "10888880"
        request.account_type = "ACCOUNT_TYPE_BUSINESS"
        request.account_bank = "农业银行"
        request.bank_address_code = "310100"
        request.account_number = "6235012141000002900"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""