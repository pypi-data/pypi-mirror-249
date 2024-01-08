import unittest
import dg_sdk
import json
from demo.demo_config import *


def getTerminalDeviceData():
    dto = dict()
    # 交易设备ip
    dto["device_ip"] = "127.0.0.1"
    # 设备类型
    dto["device_type"] = "1"
    # 交易设备gps
    # dto["device_gps"] = ""
    # 交易设备iccid
    # dto["device_icc_id"] = ""
    # 交易设备imei
    # dto["device_imei"] = ""
    # 交易设备imsi
    # dto["device_imsi"] = ""
    # 交易设备mac
    # dto["device_mac"] = ""
    # 交易设备wifimac
    # dto["device_wifi_mac"] = ""

    return json.dumps(dto)

def getRiskCheckData():
    dto = dict()
    # ip地址
    dto["ip_addr"] = "111"
    # 基站地址
    # dto["base_station"] = ""
    # 纬度
    # dto["latitude"] = ""
    # 经度
    # dto["longitude"] = ""

    return json.dumps(dto)

def getAcctSplitBunchRucan():
    dto = dict()
    # 分账信息列表
    dto["acct_infos"] = getAcctInfos()

    return json.dumps(dto)

def getAcctInfos():
    dto = dict()
    # 支付金额
    # dto["div_amt"] = ""
    # 被分账方ID
    # dto["huifu_id"] = ""
    # 账户号
    # dto["acct_id"] = ""

    dtoList = [dto]
    return dtoList

def getExtendPayData():
    dto = dict()
    # 商品简称
    dto["goods_short_name"] = "一般商品"
    # 网关支付受理渠道
    dto["gw_chnnl_tp"] = "01"
    # 业务种类
    dto["biz_tp"] = "123456"

    return json.dumps(dto)


def build_extend_infos():
    """
    非必填字段

    :return: 非必填字段组成的字典
    """
    extend_infos = dict()
    # 延时标记
    extend_infos["delay_acct_flag"] = "N"
    # 交易有效期
    extend_infos["time_expire"] = "20220406210038"
    # 分账对象
    extend_infos["acct_split_bunch"] = getAcctSplitBunchRucan()
    # 备注
    extend_infos["remark"] = ""
    # 页面失败跳转地址
    extend_infos["front_fail_url"] = "http://www.baidu.com"
    return extend_infos


class TestV2TradeOnlinepaymentWappayRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 手机WAP支付 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2TradeOnlinepaymentWappayRequest()
        request.req_date = ""
        request.req_seq_id = ""
        request.huifu_id = "6666000103124174"
        request.trans_amt = "300.01"
        request.instalments_num = "03"
        request.bank_card_no = "6222021102043040313"
        request.extend_pay_data = getExtendPayData()
        request.risk_check_data = getRiskCheckData()
        request.terminal_device_data = getTerminalDeviceData()
        request.front_url = "http://www.baidu.com"
        request.notify_url = "virgo://http://192.168.25.213:30030/sspc/onlineAsync"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""