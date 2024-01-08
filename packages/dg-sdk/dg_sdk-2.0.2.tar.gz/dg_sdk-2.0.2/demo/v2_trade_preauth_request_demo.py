import unittest
import dg_sdk
import json
from demo.demo_config import *


def getTerminalDeviceData():
    dto = dict()
    # 商户终端版本号
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
    dto["devs_id"] = "SPINTP366020000360401"
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

def getWxData():
    dto = dict()
    # 附加数据
    dto["attach"] = ""
    # 商品详情
    dto["detail"] = getWxGoodsRucan()
    # 设备号
    dto["device_info"] = ""
    # 订单优惠标记
    dto["goods_tag"] = "12321312"
    # 场景信息
    dto["scene_info"] = getWxSceneRucan()
    # 子商户公众账号ID
    dto["sub_appid"] = "wx48abf94e085e98e1"

    return json.dumps(dto)

def getWxSceneRucan():
    dto = dict()
    # 门店信息
    dto["store_info"] = getWxStoreRucan()

    return dto;

def getWxStoreRucan():
    dto = dict()
    # 门店详细地址
    dto["address"] = "汇付天下桂林路"
    # 门店行政区划码
    dto["area_code"] = "310"
    # 门店id
    dto["id"] = "1232131"
    # 门店名称
    dto["name"] = "测试"

    return dto;

def getWxGoodsRucan():
    dto = dict()
    # 单品列表
    dto["goods_detail"] = getWxGoodsDetailRucan()
    # 订单原价
    dto["cost_price"] = "1"
    # 商品小票ID
    dto["receipt_id"] = ""

    return dto;

def getWxGoodsDetailRucan():
    dto = dict()
    # 商品编码
    dto["goods_id"] = "1232131"
    # 商品名称
    dto["goods_name"] = "汇付天下"
    # 商品单价
    dto["price"] = "0.50"
    # 商品数量
    dto["quantity"] = 0
    # 微信侧商品编码
    dto["wxpay_goods_id"] = ""

    dtoList = [dto]
    return dtoList

def getAlipayData():
    dto = dict()
    # 支付宝的店铺编号
    dto["alipay_store_id"] = ""
    # 业务扩展参数
    dto["extend_params"] = getExtendParams()
    # 订单包含的商品列表信息
    dto["goods_detail"] = getAliGoodsDetail()
    # 商户操作员编号
    dto["operator_id"] = "1234567890123456789012345678"
    # 商户门店编号
    dto["store_id"] = ""

    return json.dumps(dto)

def getAliGoodsDetail():
    dto = dict()
    # 商品的编号
    dto["goods_id"] = "12345678901234567890123456789012"
    # 商品名称
    dto["goods_name"] = "111"
    # 商品单价
    dto["price"] = "1.01"
    # 商品数量
    dto["quantity"] = "1"
    # 商品描述信息
    dto["body"] = ""
    # 商品类目树
    dto["categories_tree"] = ""
    # 商品类目
    dto["goods_category"] = ""
    # 商品的展示地址
    dto["show_url"] = "321313"

    dtoList = [dto]
    return dtoList

def getExtendParams():
    dto = dict()
    # 卡类型
    dto["card_type"] = ""
    # 支付宝点餐场景类型
    dto["food_order_type"] = "qr_order"
    # 花呗分期数
    dto["hb_fq_num"] = ""
    # 手续费百分比
    dto["hb_fq_seller_percent"] = ""
    # 行业数据回流信息
    dto["industry_reflux_info"] = ""
    # 系统商编号
    dto["sys_service_provider_id"] = ""

    return json.dumps(dto)


def build_extend_infos():
    """
    非必填字段

    :return: 非必填字段组成的字典
    """
    extend_infos = dict()
    # 外部订单号
    extend_infos["out_ord_id"] = "2021031722001427671459048436"
    # 交易发起时间
    extend_infos["send_time"] = "12345678901234567"
    # 交易失效时间
    extend_infos["time_expire"] = "20221130121212"
    # 禁用信用卡标记
    extend_infos["limit_pay_type"] = "NO_CREDIT"
    # 场景类型
    extend_infos["pay_scene"] = "02"
    # 渠道号
    extend_infos["channel_no"] = ""
    # 传入分帐遇到优惠的处理规则
    extend_infos["term_div_coupon_type"] = "1"
    # 支付宝扩展参数集合
    extend_infos["alipay_data"] = getAlipayData()
    # 微信扩展参数集合
    extend_infos["wx_data"] = getWxData()
    # 商户扩展域
    extend_infos["mer_priv"] = "{\"callType\":\"01\",\"lc\":\"12345678901234567890123456789012123\",\"softVersion\":\"6.5.3\"}"
    # 备注
    extend_infos["remark"] = "123213132132"
    # 授权号
    extend_infos["auth_no"] = "608467"
    # 批次号
    extend_infos["batch_id"] = "987654"
    # 商户操作员号
    extend_infos["mer_oper_id"] = "12345678901234567890123456789012"
    # 输入密码提示
    # extend_infos["password_trade"] = ""
    # 设备信息
    extend_infos["terminal_device_data"] = getTerminalDeviceData()
    # 异步通知地址
    extend_infos["notify_url"] = "http://www.baidu.com"
    return extend_infos


class TestV2TradePreauthRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 微信支付宝预授权 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2TradePreauthRequest()
        request.req_date = ""
        request.req_seq_id = ""
        request.huifu_id = "6666000108854952"
        request.trans_amt = "0.02"
        request.goods_desc = "123213213"
        request.auth_code = "280426995846228615"
        request.risk_check_data = getRiskCheckData()

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""