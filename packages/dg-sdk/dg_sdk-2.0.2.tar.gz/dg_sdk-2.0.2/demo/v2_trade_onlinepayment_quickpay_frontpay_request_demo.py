import unittest
import dg_sdk
import json
from demo.demo_config import *


def getRiskCheckData():
    dto = dict()
    # ip地址
    dto["ip_addr"] = "127.0.0.1"
    # 基站地址
    # dto["base_station"] = ""
    # 纬度
    # dto["latitude"] = ""
    # 经度
    # dto["longitude"] = ""

    return json.dumps(dto)

def getTerminalDeviceData():
    dto = dict()
    # 设备类型
    dto["device_type"] = "1"
    # 交易设备IP
    dto["device_ip"] = "127.0.0.1"
    # 交易设备MAC
    # dto["device_mac"] = ""
    # 交易设备IMEI
    # dto["device_imei"] = ""
    # 交易设备IMSI
    # dto["device_imsi"] = ""
    # 交易设备ICCID
    # dto["device_icc_id"] = ""
    # 交易设备WIFIMAC
    # dto["device_wifi_mac"] = ""
    # 交易设备GPS
    # dto["device_gps"] = ""

    return json.dumps(dto)

def getExtendPayData():
    dto = dict()
    # 商品简称
    dto["goods_short_name"] = "01"
    # 业务种类
    dto["biz_tp"] = "123451"
    # 网关支付受理渠道
    dto["gw_chnnl_tp"] = "02"

    return json.dumps(dto)

def getAcctSplitBunchRucan():
    dto = dict()
    # 分账明细
    dto["acct_infos"] = getAcctInfos()

    return json.dumps(dto)

def getAcctInfos():
    dto = dict()
    # 被分账对象ID
    dto["huifu_id"] = "6666000109812884"
    # 分账金额
    dto["div_amt"] = "0.01"
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
    # 用户客户号
    # extend_infos["user_huifu_id"] = ""
    # 订单类型
    extend_infos["order_type"] = "P"
    # 订单失效时间
    extend_infos["time_expire"] = ""
    # 商品描述
    extend_infos["goods_desc"] = "快捷支付接口"
    # 请求类型
    extend_infos["request_type"] = "P"
    # 延时标记
    # extend_infos["delay_acct_flag"] = ""
    # 分账串
    extend_infos["acct_split_bunch"] = getAcctSplitBunchRucan()
    # 手续费扣款标志
    extend_infos["fee_flag"] = "2"
    # 备注
    extend_infos["remark"] = "remark快捷支付接口"
    # 页面跳转地址
    extend_infos["front_url"] = "http://www.baidu.com"
    return extend_infos


class TestV2TradeOnlinepaymentQuickpayFrontpayRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 快捷支付页面版接口 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2TradeOnlinepaymentQuickpayFrontpayRequest()
        request.req_seq_id = ""
        request.req_date = ""
        request.huifu_id = "6666000109812884"
        request.trans_amt = "0.01"
        request.extend_pay_data = getExtendPayData()
        request.terminal_device_data = getTerminalDeviceData()
        request.risk_check_data = getRiskCheckData()
        request.notify_url = "http://www.baidu.com"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""