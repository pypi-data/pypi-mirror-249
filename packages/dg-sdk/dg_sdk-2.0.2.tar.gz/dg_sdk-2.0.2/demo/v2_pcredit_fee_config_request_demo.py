import unittest
import dg_sdk
import json
from demo.demo_config import *


def getHbFqFeeList():
    dto = dict()
    # 商户汇付Id
    dto["huifu_id"] = "6666000003156435"
    # 花呗分期状态
    # dto["hb_fq_status"] = ""
    # 花呗分期3期开关
    dto["hb_three_period_switch"] = "Y"
    # 花呗收单分期3期费率（%）
    dto["hb_three_acq_period"] = "5"
    # 花呗分期3期利率（%）
    dto["hb_three_period"] = "10"
    # 花呗分期6期开关
    dto["hb_six_period_switch"] = "Y"
    # 花呗收单分期6期费率（%）
    dto["hb_six_acq_period"] = "5"
    # 花呗分期6期利率（%）
    dto["hb_six_period"] = "10"
    # 花呗分期12期开关
    dto["hb_twelve_period_switch"] = "Y"
    # 花呗收单分期12期费率（%）
    dto["hb_twelve_acq_period"] = "15"
    # 花呗分期12期利率（%）
    dto["hb_twelve_period"] = "11"
    # 交易手续费外扣标记
    dto["out_fee_flag"] = ""
    # 手续费外扣的汇付商户号
    dto["out_fee_huifu_id"] = ""

    dtoList = [dto]
    return json.dumps(dtoList)

def getBankFqList():
    dto = dict()
    # 银联入网模式
    dto["ent_way"] = "1"
    # 商户汇付Id
    dto["huifu_id"] = "6666000003156435"
    # 银行卡分期状态
    dto["bank_card_fq_status"] = "1"
    # 银行卡分期费率
    dto["bank_fq_fee_list"] = getBankFqFeeList()
    # 贴息模式
    dto["fee_model"] = "1"

    dtoList = [dto]
    return json.dumps(dtoList)

def getBankFqFeeList():
    dto = dict()
    # 银行编号
    dto["bank_code"] = "01040000"
    # 银行名称
    dto["bank_name"] = ""
    # 银联收单分期费率（%）
    dto["bank_acq_period"] = "6"
    # 用户付息费率
    dto["bank_fee_rate"] = "2"
    # 交易手续费外扣标记
    dto["out_fee_flag"] = ""
    # 手续费外扣的汇付商户号
    dto["out_fee_huifu_id"] = ""
    # 银联分期3期开关
    dto["three_period_switch"] = "Y"
    # 银联分期3期总费率（%）
    dto["three_period"] = "10"
    # 银联分期6期开关
    dto["six_period_switch"] = "Y"
    # 银联分期6期总费率（%）
    dto["six_period"] = "16"
    # 银联分期12期开关
    dto["twelve_period_switch"] = "Y"
    # 银联分期12期总费率（%）
    dto["twelve_period"] = "0.0001"

    dtoList = [dto]
    return dtoList


def build_extend_infos():
    """
    非必填字段

    :return: 非必填字段组成的字典
    """
    extend_infos = dict()
    # 异步通知地址
    extend_infos["async_return_url"] = "http://192.168.85.157:30031/sspm/testVirgo"
    # 银行分期费率
    extend_infos["bank_fq_list"] = getBankFqList()
    # 花呗分期费率
    extend_infos["hb_fq_fee_list"] = getHbFqFeeList()
    return extend_infos


class TestV2PcreditFeeConfigRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 商户分期配置 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2PcreditFeeConfigRequest()
        request.req_date = ""
        request.req_seq_id = ""

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""