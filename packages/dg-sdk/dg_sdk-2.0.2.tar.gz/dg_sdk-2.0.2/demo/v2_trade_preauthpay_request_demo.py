import unittest
import dg_sdk
import json
from demo.demo_config import *


def getTerminalDeviceData():
    dto = dict()
    # 商户终端序列号
    dto["app_version"] = ""
    # 交易设备GPS
    dto["device_gps"] = ""
    # 交易设备ICCID
    dto["device_icc_id"] = ""
    # 交易设备IMEI
    dto["device_imei"] = ""
    # 交易设备IMSI
    dto["device_imsi"] = ""
    # 交易设备IP
    dto["device_ip"] = "10.10.0.1"
    # 交易设备MAC
    dto["device_mac"] = ""
    # 设备类型
    dto["device_type"] = "1"
    # 交易设备WIFIMAC
    dto["device_wifi_mac"] = ""
    # 汇付机具号
    dto["devs_id"] = ""
    # ICCID
    dto["icc_id"] = ""
    # 商户终端实时经纬度信息
    dto["location"] = "+32.10520/+118.80593"
    # 商户交易设备IP
    dto["mer_device_ip"] = ""
    # 商户设备类型
    dto["mer_device_type"] = "01"
    # 移动国家代码
    dto["mobile_country_cd"] = ""
    # 移动网络号码
    dto["mobile_net_num"] = ""
    # 商户终端入网认证编号
    dto["network_license"] = "P3111"
    # 商户终端序列号
    dto["serial_num"] = ""

    return json.dumps(dto)

def getRiskCheckData():
    dto = dict()
    # 基站地址
    dto["base_station"] = "192.168.1.1"
    # ip地址
    dto["ip_addr"] = "180.167.105.130"
    # 纬度
    dto["latitude"] = "33.3"
    # 经度
    dto["longitude"] = "33.3"

    return json.dumps(dto)


def build_extend_infos():
    """
    非必填字段

    :return: 非必填字段组成的字典
    """
    extend_infos = dict()
    # 外部订单号
    extend_infos["out_ord_id"] = "12345678901234567890123456789012"
    # 原授权号
    extend_infos["org_auth_no"] = ""
    # 原预授权交易请求流水号
    extend_infos["org_req_seq_id"] = ""
    # 预授权汇付全局流水号
    extend_infos["pre_auth_hf_seq_id"] = "0029000topB221031163126P798c0a8305400000"
    # 备注
    extend_infos["remark"] = "123451111"
    # 批次号
    # extend_infos["batch_id"] = ""
    # 商户操作员号
    # extend_infos["mer_oper_id"] = ""
    # 扩展域
    # extend_infos["mer_priv"] = ""
    # 设备信息
    extend_infos["terminal_device_data"] = getTerminalDeviceData()
    # 异步通知地址
    extend_infos["notify_url"] = "http://www.baidu.com"
    return extend_infos


class TestV2TradePreauthpayRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 微信支付宝预授权完成 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2TradePreauthpayRequest()
        request.req_date = ""
        request.req_seq_id = ""
        request.huifu_id = "6666000108854952"
        request.org_req_date = "20221031"
        request.trans_amt = "0.02"
        request.goods_desc = "1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567"
        request.risk_check_data = getRiskCheckData()

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""