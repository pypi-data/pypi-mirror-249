import unittest
import dg_sdk
import json
from demo.demo_config import *


def getTrxDeviceInf():
    dto = dict()
    # 银行预留手机号
    dto["trx_mobile_num"] = "15556622368"
    # 设备类型
    dto["trx_device_type"] = "1"
    # 交易设备IP
    dto["trx_device_ip"] = "10.10.0.1"
    # 交易设备MAC
    dto["trx_device_mac"] = "10.10.0.1"
    # 交易设备IMEI
    dto["trx_device_imei"] = "030147441006000182623"
    # 交易设备IMSI
    dto["trx_device_imsi"] = "030147441006000182623"
    # 交易设备ICCID
    dto["trx_device_icc_id"] = "030147441006000182623"
    # 交易设备WIFIMAC
    dto["trx_device_wfifi_mac"] = "030147441006000182623"
    # 交易设备GPS
    dto["trx_device_gps"] = "030147441006000182623"

    return json.dumps(dto)

def getRiskInfo():
    dto = dict()
    # IP类型
    # dto["ip_type"] = "test"
    # IP值
    # dto["source_ip"] = "test"
    # 设备标识
    # dto["device_id"] = ""
    # 设备类型
    # dto["device_type"] = ""
    # 应用提供方账户ID
    # dto["account_id_hash"] = ""
    # 银行预留手机号
    # dto["mobile"] = ""

    return json.dumps(dto)


def build_extend_infos():
    """
    非必填字段

    :return: 非必填字段组成的字典
    """
    extend_infos = dict()
    # 证件有效期类型
    extend_infos["cert_validity_type"] = "0"
    # 证件有效期起始日
    extend_infos["cert_begin_date"] = "20170121"
    # 挂网协议编号
    extend_infos["protocol_no"] = ""
    # 风控信息
    # extend_infos["risk_info"] = getRiskInfo()
    # 回调页面地址
    # extend_infos["verify_front_url"] = ""
    return extend_infos


class TestV2QuickbuckleOnekeyCardbindRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 一键绑卡 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2QuickbuckleOnekeyCardbindRequest()
        request.req_seq_id = ""
        request.req_date = ""
        request.huifu_id = "6666000003078984"
        request.out_cust_id = "6666000103633619"
        request.bank_id = "01030000"
        request.card_name = "YTRf65hBDkH9UU1AwG16r4Nlc/X1rH6ejKbvmqT80exJ6whdHI1zB+izBtNBOJfhRNbIOhi1FrRuE5b7wnt/03Q+vwWQQLDGJXWZf92yp+eIRDHg8JdbjOgxKvF2q4Qw5704jbsjQm4UJW5fqRhzRPtnnAL9zzTSgVhuQ0KCwc8="
        request.cert_id = "gk8zqa+zvIUAvzV3Bjzzw+vRgq2LgTzQI8PRoqUdbeuFMbFZ6LllQpcOhWIz6F82VtFBKzLd5kPOaCwlQCiwsXhSqUFB11zgzKUtVIuiv9lHY/EsjRwqDBhgeR5f2H9FXr3wQ9f7bI7t8ca9o93QxrXr/1MDBq7fGok0xu2ytsM="
        request.cert_type = "00"
        request.cert_end_date = "20370121"
        request.card_mp = "e2zKkJ6PE6UtZhgz42pqgPLQh6p83/WJsG7EVSgYYgN+7MIiCzXnjTpmpv0Cgv7cYTbQTBf/NF5jqeI8BpFjP7C6gg+0cjqW2tgdVxyfqZLu2fEJRth7NgZKgS2ZKbkZ8PNfUk7V+aHbqkAVKY92bdcSQSNIuWaJCeIF34w+l+k="
        request.dc_type = "D"
        request.async_return_url = "http://192.168.85.157:30031/sspm/testVirgo"
        request.trx_device_inf = getTrxDeviceInf()

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""