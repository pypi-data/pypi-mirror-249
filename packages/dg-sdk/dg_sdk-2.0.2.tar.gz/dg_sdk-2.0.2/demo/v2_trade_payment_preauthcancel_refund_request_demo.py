import unittest
import dg_sdk
import json
from demo.demo_config import *


def getTerminalDeviceInfo():
    dto = dict()
    # 交易设备GPS
    dto["device_gps"] = "192.168.0.0"
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
    dto["devs_id"] = "SPINTP366061800405501"
    # 操作员号
    dto["mer_oper_id"] = ""
    # 逻辑终端号
    dto["pnr_dev_id"] = ""

    return dto;

def getRiskCheckInfo():
    dto = dict()
    # 基站地址
    dto["base_station"] = "192.168.1.1"
    # ip地址
    dto["ip_addr"] = "192.168.1.1"
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
    extend_infos["out_ord_Id"] = ""
    # 原授权号
    extend_infos["org_auth_no"] = ""
    # 原交易请求流水号
    extend_infos["org_req_seq_id"] = ""
    # 原预授权全局流水号
    extend_infos["pre_auth_hf_seq_id"] = "0029000topB221031162644P959c0a8305400000"
    # 批次号
    extend_infos["batch_id"] = ""
    # 商品描述
    extend_infos["good_desc"] = ""
    # 备注
    extend_infos["remark"] = ""
    # 交易发起时间
    extend_infos["send_time"] = ""
    # 是否人工介入
    extend_infos["is_manual_process"] = "Y"
    # 汇付机具号
    extend_infos["devs_id"] = "SPINTP366020000360401"
    # 商户操作员号
    # extend_infos["mer_oper_id"] = ""
    # 扩展域
    # extend_infos["mer_priv"] = ""
    # 设备信息
    extend_infos["terminal_device_info"] = getTerminalDeviceInfo()
    # 异步通知地址
    extend_infos["notify_url"] = "http://www.baidu.com"
    return extend_infos


class TestV2TradePaymentPreauthcancelRefundRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 微信支付宝预授权撤销 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2TradePaymentPreauthcancelRefundRequest()
        request.req_date = ""
        request.req_seq_id = ""
        request.huifu_id = "6666000108854952"
        request.org_req_date = "20221031"
        request.ord_amt = "0.02"
        request.risk_check_info = getRiskCheckInfo()

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""