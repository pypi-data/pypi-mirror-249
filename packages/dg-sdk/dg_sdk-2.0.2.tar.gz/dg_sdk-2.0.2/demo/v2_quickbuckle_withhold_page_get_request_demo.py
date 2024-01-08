import unittest
import dg_sdk
import json
from demo.demo_config import *


def getRiskInfo():
    dto = dict()
    # IP类型
    dto["ip_type"] = "04"
    # IP值
    dto["source_ip"] = "1.1.1.1"
    # 设备标识
    dto["device_id"] = ""
    # 设备类型
    dto["device_type"] = ""
    # 银行预留手机号
    dto["mobile"] = ""

    return json.dumps(dto)

def getTrxDeviceInfo():
    dto = dict()
    # 银行预留手机号
    dto["trx_mobile_num"] = "13428722321"
    # 设备类型
    dto["trx_device_type"] = "1"
    # 交易设备IP
    dto["trx_device_ip"] = "192.168.1.1"
    # 交易设备MAC
    dto["trx_device_mac"] = "10.10.0.1"
    # 交易设备IMEI
    dto["trx_device_imei"] = "imei"
    # 交易设备IMSI
    dto["trx_device_imsi"] = "imsi"
    # 交易设备ICCID
    dto["trx_device_icc_id"] = "icc"
    # 交易设备WIFIMAC
    dto["trx_device_wfifi_mac"] = "wfifi"
    # 交易设备GPS
    dto["trx_device_gps"] = "gps"

    return json.dumps(dto)


def build_extend_infos():
    """
    非必填字段

    :return: 非必填字段组成的字典
    """
    extend_infos = dict()
    # 页面有效期
    extend_infos["expire_time"] = "20"
    # 页面跳转地址
    extend_infos["return_url"] = "https://api.huifu.com"
    # 客户用户号
    extend_infos["out_cust_id"] = "Q837467382819"
    # 用户汇付号
    extend_infos["user_huifu_id"] = "6666000107386236"
    # 异步通知地址
    extend_infos["notify_url"] = "https://api.huifu.com"
    # 设备信息域
    extend_infos["trx_device_info"] = getTrxDeviceInfo()
    # 风控信息
    extend_infos["risk_info"] = getRiskInfo()
    return extend_infos


class TestV2QuickbuckleWithholdPageGetRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 代扣绑卡页面版 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2QuickbuckleWithholdPageGetRequest()
        request.req_seq_id = ""
        request.req_date = ""
        request.huifu_id = "6666000103422897"
        request.order_id = "SAS20230807102136898274149"
        request.order_date = "20230807"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""