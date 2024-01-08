import unittest
import dg_sdk
import json
from demo.demo_config import *


def getTerminalDeviceData():
    dto = dict()
    # 交易设备ip
    dto["device_ip"] = "172.31.31.145"
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
    # 基站地址经纬度、基站地址、IP地址三组信息至少填写一组；&lt;br/&gt;【mcc】+【mnc】+【location_cd】+【lbs_num】&lt;br/&gt;- mcc:移动国家代码，460代表中国；3位长&lt;br/&gt;- mnc：移动网络号码；2位长；&lt;br/&gt;- location_cd：位置区域码，16进制，5位长&lt;br/&gt;- lbs_num：基站编号，16进制，5位长&lt;br/&gt;- 注意若位数不足用空格补足；&lt;br/&gt;&lt;font color&#x3D;&quot;green&quot;&gt;示例值：460001039217563&lt;/font&gt;，460（mcc)， 00(mnc)，10392(location_cd)， 17563(lbs_num)
    dto["base_station"] = ""
    # ip地址经纬度、基站地址、IP地址三组信息至少填写一组；&lt;font color&#x3D;&quot;green&quot;&gt;示例值：172.28.52.52&lt;/font&gt;
    dto["ip_addr"] = "192.168.1.1"
    # 纬度纬度整数位不超过2位，小数位不超过6位。格式为：+表示北纬，-表示南纬。&lt;font color&#x3D;&quot;green&quot;&gt;示例值：+37.12&lt;/font&gt;；&lt;br/&gt;经纬度、基站地址、IP地址三组信息至少填写一组
    dto["latitude"] = ""
    # 经度经度整数位不超过3位，小数位不超过5位；格式为:+表示东经，-表示西经。&lt;font color&#x3D;&quot;green&quot;&gt;示例值：-121.213&lt;/font&gt;；&lt;br/&gt;经纬度、基站地址、IP地址三组信息至少填写一组
    dto["longitude"] = ""

    return json.dumps(dto)

def getExtendPayData():
    dto = dict()
    # 业务种类
    dto["biz_tp"] = "012345"
    # 商品简称
    dto["goods_short_name"] = "看看"
    # 网关支付受理渠道
    # dto["gw_chnnl_tp"] = "test"

    return json.dumps(dto)

def getAcctSplitBunch():
    dto = dict()
    # 分账信息列表
    # dto["acct_infos"] = getAcctInfos()

    return dto;

def getAcctInfos():
    dto = dict()
    # 支付金额
    # dto["div_amt"] = ""
    # 商户号
    # dto["huifu_id"] = ""

    dtoList = [dto]
    return dtoList


def build_extend_infos():
    """
    非必填字段

    :return: 非必填字段组成的字典
    """
    extend_infos = dict()
    # 备注
    extend_infos["remark"] = "reamrk123"
    # 账户号
    # extend_infos["acct_id"] = ""
    # 订单失效时间
    extend_infos["time_expire"] = "20221212121212"
    # 分账对象
    # extend_infos["acct_split_bunch"] = getAcctSplitBunch()
    return extend_infos


class TestV2TradeOnlinepaymentWithholdpayRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 代扣支付 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2TradeOnlinepaymentWithholdpayRequest()
        request.req_date = ""
        request.req_seq_id = ""
        request.huifu_id = "6666000109812884"
        request.user_huifu_id = "6666000109818115"
        request.card_bind_id = "10024597199"
        request.trans_amt = "0.01"
        request.goods_desc = "代扣test"
        request.withhold_type = "2"
        request.extend_pay_data = getExtendPayData()
        request.risk_check_data = getRiskCheckData()
        request.terminal_device_data = getTerminalDeviceData()
        request.notify_url = "http://www.chinapnr.com/"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""