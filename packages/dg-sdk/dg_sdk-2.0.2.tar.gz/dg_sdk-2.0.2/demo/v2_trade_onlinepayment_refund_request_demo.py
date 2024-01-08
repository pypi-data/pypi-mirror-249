import unittest
import dg_sdk
import json
from demo.demo_config import *


def getRiskCheckData():
    dto = dict()
    # ip地址
    # dto["ip_addr"] = ""
    # 基站地址
    # dto["base_station"] = ""
    # 纬度
    # dto["latitude"] = ""
    # 经度
    # dto["longitude"] = ""

    return json.dumps(dto)

def getTerminalDeviceData():
    dto = dict()
    # 交易设备ip
    dto["device_ip"] = "172.31.31.145"
    # 设备类型
    dto["device_type"] = "1"
    # 交易设备gps
    dto["device_gps"] = "07"
    # 交易设备iccid
    dto["device_icc_id"] = "05"
    # 交易设备imei
    dto["device_imei"] = "02"
    # 交易设备imsi
    dto["device_imsi"] = "03"
    # 交易设备mac
    dto["device_mac"] = "01"
    # 交易设备wifimac
    dto["device_wifi_mac"] = "06"

    return json.dumps(dto)

def getBankInfoData():
    dto = dict()
    # 付款方账户类型
    # dto["card_acct_type"] = "test"
    # 省份
    # dto["province"] = ""
    # 地区
    # dto["area"] = ""
    # 银行编号
    # dto["bank_code"] = ""
    # 联行号
    # dto["correspondent_code"] = ""

    return json.dumps(dto)

def getCombinedpayData():
    dto = dict()
    # 补贴方汇付编号
    # dto["huifu_id"] = "test"
    # 补贴方类型
    # dto["user_type"] = "test"
    # 补贴方账户号
    # dto["acct_id"] = "test"
    # 补贴金额
    # dto["amount"] = "test"

    dtoList = [dto]
    return json.dumps(dtoList)

def getAcctSplitBunchRucan():
    dto = dict()
    # 分账信息列表
    # dto["acct_infos"] = getAcctInfosRucan()

    return json.dumps(dto)

def getAcctInfosRucan():
    dto = dict()
    # 商户号
    # dto["huifu_id"] = ""
    # 支付金额
    # dto["div_amt"] = ""

    dtoList = [dto]
    return dtoList


def build_extend_infos():
    """
    非必填字段

    :return: 非必填字段组成的字典
    """
    extend_infos = dict()
    # 原交易请求日期
    extend_infos["org_req_date"] = "20221110"
    # 原交易全局流水号
    extend_infos["org_hf_seq_id"] = ""
    # 原交易请求流水号
    extend_infos["org_req_seq_id"] = "RQ1212333113"
    # 分账对象
    extend_infos["acct_split_bunch"] = getAcctSplitBunchRucan()
    # 补贴支付信息
    extend_infos["combinedpay_data"] = getCombinedpayData()
    # 大额转账支付账户信息数据
    # extend_infos["bank_info_data"] = getBankInfoData()
    # 备注
    extend_infos["remark"] = "remark123"
    # 异步通知地址
    extend_infos["notify_url"] = "http://www.baidu.com"
    return extend_infos


class TestV2TradeOnlinepaymentRefundRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 线上交易退款 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2TradeOnlinepaymentRefundRequest()
        request.req_date = ""
        request.req_seq_id = ""
        request.huifu_id = "6666000108854952"
        request.ord_amt = "0.01"
        request.terminal_device_data = getTerminalDeviceData()
        request.risk_check_data = getRiskCheckData()

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""