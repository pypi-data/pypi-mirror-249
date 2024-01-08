import unittest
import dg_sdk
import json
from demo.demo_config import *


def getRiskInfo():
    dto = dict()
    # IP类型
    dto["ip_type"] = "04"
    # IP值
    dto["source_ip"] = "192.168.1.2"
    # 设备标识
    dto["device_id"] = "123"
    # 设备类型
    dto["device_type"] = "1"
    # 银行预留手机号
    dto["mobile"] = "13778787106"

    return json.dumps(dto)

def getTrxDeviceInfo():
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

    return dto;


def build_extend_infos():
    """
    非必填字段

    :return: 非必填字段组成的字典
    """
    extend_infos = dict()
    # 页面有效期
    extend_infos["expire_time"] = "15"
    # 设备信息域
    extend_infos["trx_device_info"] = getTrxDeviceInfo()
    # 风控信息
    extend_infos["risk_info"] = getRiskInfo()
    return extend_infos


class TestV2QuickbuckleWithholdApplyRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 代扣绑卡申请 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2QuickbuckleWithholdApplyRequest()
        request.req_seq_id = ""
        request.req_date = ""
        request.huifu_id = "6666000003078984"
        request.return_url = "http://www.huifu1234.com/"
        request.out_cust_id = "16666000106789536"
        request.order_id = "20230525081932677893621"
        request.order_date = "20230525"
        request.card_id = "ZSSW+34A2soLbwLQ5SkZJO4Azy6BknTGkk6EYDTbGA+G0v+zcF3TnU4iYH171KB4ReLjJlY+hSy8MvgVbAx7dL9V7LvLFJd8RE+Lp6XKiIbVUCA1wd2Otp2jI2D32z5gUFqUbB4clRZyRyltXV3xmAWH4fLZDER3H+QwC0/UNF4="
        request.card_name = "H12ShtAyV4I4sOQqbISH4eMQUcmzpYOHggxRcXhxNoForh5qLyFgDrsSTn0nnepnPO8okfZYSWQlWIBzsRyyHYwAk94s2sO2Sz/6q4Jg2xDieeGDGrnrAphc8/OAN2OK8dMdbQzL12MvPQU/GX148MCxJzGvvdRFqTEPRLOLXTs="
        request.cert_type = "00"
        request.cert_id = "FviSPp2Xv6QYfRSYRZcouGAz4BvfZRS9nFKI/7daIUtn4JmBVMTDtrqKLCWeoY7WP4hQAz3rptjOe8WsuynRG3kQhBsXZB0v6e1X1+POD5FXVojquKQb1BF5tKlaOqTj/+G62URC3SWui26JzQQmjGhCORXXHFD7PPNJKusYhHI="
        request.card_mp = "GmMLD+v2Mfc/vr9HOVFKOon3Dl4Q9cjze21X902G8Dnl2/2rpH8wpJUnufoYnI0nR9D2XkOm0ApOJL3ShiZxgLvnTaKrTDjRdrBJexhXbbhbfDx/2x+ZULvZHOEjzRI21tK2WKUzxDhX/lw/iXMjslKNVYlQ7as/aH5bLipf12g="
        request.vip_code = "HOVFKOon3Dl4Q9cjze21X902G8Dnl2LvLFJd8RE+Lp6XKiIbVUCA1wd2Otp2jI2D32z5gUFqUbB4clRZyRyltXV3xmAWH4fLZDER3H+YwAk94s2sO2Sz/6q4Jg2xDieesO2Sz/6q4Jg2xDieeGDGbQzL12MvPQU/GX14xJzGvvd="
        request.expiration = "IUtn4JmBVMTDtrqKLCWeoY7WP4hQAz3rptjOe8WsuySW+34SkZJO4Azy6BknTGkk6EA2soLbwLQ5SkZJO4Azy6BknTGkk6EX902G8Dnl2/2rpH8wpJUnufoYnI0nR9YDTbGA+G0v+ApOJL3ShiZxgLvnTaKrnU4iYH171KB4="
        request.cert_validity_type = "0"
        request.cert_begin_date = "20140504"
        request.cert_end_date = "20260504"
        request.dc_type = "test"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""