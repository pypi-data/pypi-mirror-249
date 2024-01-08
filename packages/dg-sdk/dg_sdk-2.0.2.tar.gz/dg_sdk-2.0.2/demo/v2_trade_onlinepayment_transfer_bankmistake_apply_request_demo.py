import unittest
import dg_sdk
import json
from demo.demo_config import *


def getBankInfoData():
    dto = dict()
    # 银行编号
    dto["bank_code"] = "03080000"
    # 联行号选填，参见：[银行支行编码](https://paas.huifu.com/partners/api/#/csfl/api_csfl_yhzhbm)； &lt;font color&#x3D;&quot;green&quot;&gt;示例值：102290026507&lt;/font&gt;&lt;br/&gt;对私代发非必填；
    dto["correspondent_code"] = "103290076178"
    # 对公对私标识
    dto["card_acct_type"] = "P"
    # 省份
    dto["province"] = "0031"
    # 地区
    dto["area"] = "3100"
    # 支行名
    dto["subbranch_bank_name"] = "中国农业银行股份有限公司上海联洋支行"
    # 证件类型
    dto["certificate_type"] = "01"
    # 付款方三证合一码
    dto["bank_acct_three_in_one"] = "92650109MA79R8E308"
    # 手机号
    dto["mobile_no"] = "oO6XYz…………Is3nZb/5dFj860Z+nQ=="
    # 证件号
    dto["certify_no"] = "yL09mhS5…………WK04Kdfyg=="

    return json.dumps(dto)


def build_extend_infos():
    """
    非必填字段

    :return: 非必填字段组成的字典
    """
    extend_infos = dict()
    # 汇款凭证文件名称
    extend_infos["file_name"] = "汇付电子小票验证.jpg"
    # 备注
    extend_infos["remark"] = "大额转账补入账验证"
    # 银行信息数据
    extend_infos["bank_info_data"] = getBankInfoData()
    return extend_infos


class TestV2TradeOnlinepaymentTransferBankmistakeApplyRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 银行大额转账差错申请 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2TradeOnlinepaymentTransferBankmistakeApplyRequest()
        request.req_seq_id = ""
        request.req_date = ""
        request.huifu_id = "6666000110468104"
        request.trans_amt = "0.01"
        request.order_type = "REFUND"
        request.org_req_seq_id = "202308312345678931"
        request.org_req_date = "20230831"
        request.remit_date = "20230615"
        request.certificate_name = "孙洁"
        request.bank_card_no = "V2olJv4Srh…………78M8A=="
        request.bank_name = "招商银行"
        request.notify_url = "http://www.baidu.com"
        request.goods_desc = "test"
        request.certificate_content = "/9j/4QCARXhpZgAATU0…………AAB//2Q=="

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""