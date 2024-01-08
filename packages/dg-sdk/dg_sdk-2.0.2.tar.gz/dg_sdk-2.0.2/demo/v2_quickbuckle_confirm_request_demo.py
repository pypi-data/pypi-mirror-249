import unittest
import dg_sdk
import json
from demo.demo_config import *


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
    # 银行预留手机号
    # dto["mobile"] = ""

    return json.dumps(dto)

def getTrxDeviceInf():
    dto = dict()
    # 银行预留手机号
    # dto["trx_mobile_num"] = "test"
    # 设备类型
    # dto["trx_device_type"] = "test"
    # 交易设备IP
    # dto["trx_device_ip"] = "test"
    # 交易设备MAC
    # dto["trx_device_mac"] = ""
    # 交易设备IMEI
    # dto["trx_device_imei"] = ""
    # 交易设备IMSI
    # dto["trx_device_imsi"] = ""
    # 交易设备ICCID
    # dto["trx_device_icc_id"] = ""
    # 交易设备WIFIMAC
    # dto["trx_device_wfifi_mac"] = ""
    # 交易设备GPS
    # dto["trx_device_gps"] = ""

    return json.dumps(dto)


def build_extend_infos():
    """
    非必填字段

    :return: 非必填字段组成的字典
    """
    extend_infos = dict()
    # 商户名称
    extend_infos["merch_name"] = "测试"
    # 验卡流水号
    extend_infos["trans_id"] = "20220408105303542461831"
    # 卡的借贷类型
    # extend_infos["dc_type"] = ""
    # 风控信息
    # extend_infos["risk_info"] = getRiskInfo()
    return extend_infos


class TestV2QuickbuckleConfirmRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 快捷绑卡确认接口 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2QuickbuckleConfirmRequest()
        request.req_date = ""
        request.req_seq_id = ""
        request.huifu_id = "6666000003078984"
        request.out_cust_id = "6666000103633622"
        request.order_id = "20220408105303542461831"
        request.order_date = "20220408"
        request.card_id = "Ly+fnExeyPOTzfOtgRRur77nJB9TAe4PGgK9MB96o3LW2xINIxSA+B1jXDyvKNmJ5iE3wL+bbNoGd6tQXn6fmrY4vgeX8diCtP0PQVyS4UZkXzH4w8twgI+FduIukqTTl7o5/rrnL3H1HaP/Vutw3yBWrGq0l0NTebfc6XJXZss="
        request.card_name = "CDszEs+NOr7m3rh7qJhciqMN4mP1yXJtwXX6HFzBJ3rwJYUxSXFEv4f6AAQychfVPB2BgZeEoK6gtjrTPfv4G3SHqoow0Way6kdsGZYmXotcq1TFmmL+QKJSAhE4tl+vs69wCHh/l4X+Rxp4AyDK7zb8XG1GWOZOwshU/SOUukM="
        request.cert_type = "00"
        request.cert_id = "EXDKKVOSFZCFyB5p7VWlYYH+M1Y2dg9PzVBtX9LqF3w4NWtWg/id+XTFtLuC2ntaflB9ioohwPUuiSg/mp15MKV86u7/DPT84DuM/NTOTRS/ajO8rJ1ERhtyRxT5czJWGbpysQOBA+msxOjIG5k0MkP18nZDhpg07HoGArjmp08="
        request.card_mp = "Qb6AcD/EaT0gKP7d2ercByeTw2oe5loZayPuKEzQi75nZKxCyJPoIvUHTvFLRqpLDNzkpvy/aAg6xvbsw1WXdKYWB15D9LpCnYQ7qHw16IjfnPA4FDR3CE5h+nU6lGoJDj+hNRkn3y73aCeNpp5E//uDKJdjrJv6ciACf4lofAo="
        request.verify_code = "111111"
        request.vip_code = "BndOZvPCXIMcRJi1uCkw4DiNHht+KkARa+sbKbiLh4cXhjywxYM8GMl7g1a5cc1aD2PD6rVvnGzhhgpJ8mzeb/gbzNcYbU5hEXJZm5HShghGucQJB/SoqCIlyaWlz3hnclaGzznWJa5qNa50mCxVqX4zbpuGPWXv+8AnYTu8/Vk="
        request.expiration = "test"
        request.trx_device_inf = getTrxDeviceInf()

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""