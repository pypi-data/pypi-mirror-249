import unittest
import dg_sdk
import json
from demo.demo_config import *


def getTerminalDeviceData():
    dto = dict()
    # 设备类型
    dto["device_type"] = "1"
    # 交易设备ip
    dto["device_ip"] = "106.33.180.238"
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
    dto["ip_addr"] = "106.33.180.238"
    # 基站地址
    # dto["base_station"] = ""
    # 纬度
    # dto["latitude"] = ""
    # 经度
    # dto["longitude"] = ""

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
    # dto["acct_infos"] = getAcctInfos()

    return json.dumps(dto)

def getAcctInfos():
    dto = dict()
    # 分账金额
    # dto["div_amt"] = ""
    # 被分账方ID
    # dto["huifu_id"] = ""
    # 账户号
    # dto["acct_id"] = ""

    dtoList = [dto]
    return dtoList

def getExtendPayData():
    dto = dict()
    # 业务种类
    # dto["biz_tp"] = "test"
    # 商品简称
    # dto["goods_short_name"] = "test"
    # 网关支付受理渠道
    dto["gw_chnnl_tp"] = "99"

    return json.dumps(dto)


def build_extend_infos():
    """
    非必填字段

    :return: 非必填字段组成的字典
    """
    extend_infos = dict()
    # 订单类型
    # extend_infos["order_type"] = ""
    # 备注
    # extend_infos["remark"] = ""
    # 订单失效时间
    # extend_infos["time_expire"] = ""
    # 分账对象
    # extend_infos["acct_split_bunch"] = getAcctSplitBunchRucan()
    # 是否延迟交易
    # extend_infos["delay_acct_flag"] = ""
    # 手续费扣款标志
    # extend_infos["fee_flag"] = ""
    # 补贴支付信息
    # extend_infos["combinedpay_data"] = getCombinedpayData()
    return extend_infos


class TestV2TradeOnlinepaymentQuickpayApplyRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 快捷支付申请 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2TradeOnlinepaymentQuickpayApplyRequest()
        request.req_date = ""
        request.req_seq_id = ""
        request.huifu_id = "6666000119640000"
        request.user_huifu_id = "6666000121370000"
        request.card_bind_id = "10032850000"
        request.trans_amt = "1980.00"
        request.extend_pay_data = getExtendPayData()
        request.risk_check_data = getRiskCheckData()
        request.terminal_device_data = getTerminalDeviceData()
        request.notify_url = "http://tianyi.demo.test.cn/core/extend/BsPaySdk/notify_quick.php"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""