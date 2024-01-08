import unittest
import dg_sdk
import json
from demo.demo_config import *


def getTerminalDeviceInfo():
    dto = dict()
    # 商户设备类型
    # dto["mer_device_type"] = "test"
    # 汇付机具号
    # dto["devs_id"] = "test"
    # 设备类型
    dto["device_type"] = "4"
    # 交易设备IP
    dto["device_ip"] = "10.10.0.1"
    # 交易设备MAC
    dto["device_mac"] = "030147441006000182623"
    # 交易设备IMEI
    dto["device_imei"] = "030147441006000182623"
    # 交易设备IMSI
    dto["device_imsi"] = "030147441006000182623"
    # 交易设备ICCID
    dto["device_icc_id"] = "030147441006000182623"
    # 交易设备WIFIMAC
    dto["device_wifi_mac"] = "030147441006000182623"
    # 交易设备GPS
    dto["device_gps"] = "111"
    # 商户终端应用程序版
    # dto["app_version"] = ""
    # 加密随机因子
    # dto["encrypt_rand_num"] = ""
    # SIM 卡卡号
    # dto["icc_id"] = ""
    # 商户终端实时经纬度信息
    # dto["location"] = ""
    # 商户交易设备IP
    # dto["mer_device_ip"] = ""
    # 移动国家代码
    # dto["mobile_country_cd"] = ""
    # 移动网络号码
    # dto["mobile_net_num"] = ""
    # 商户终端入网认证编号
    # dto["network_license"] = ""
    # 密文数据
    # dto["secret_text"] = ""
    # 商户终端序列号
    # dto["serial_num"] = ""

    return json.dumps(dto)

def getRiskCheckData():
    dto = dict()
    # ip地址
    # dto["ip_addr"] = ""
    # 基站地址
    dto["base_station"] = "3"
    # 纬度
    dto["latitude"] = "2"
    # 经度
    dto["longitude"] = "1"

    return json.dumps(dto)

def getUnionpayData():
    dto = dict()
    # 币种
    # dto["currency_code"] = ""
    # 支持发票
    # dto["invoice_st"] = ""
    # 商户类别
    # dto["mer_cat_code"] = ""
    # 银联参数集合
    # dto["pnrins_id_cd"] = ""
    # 特殊计费信息
    # dto["specfeeinfo"] = ""
    # 终端号
    # dto["term_id"] = ""

    return json.dumps(dto)

def getAlipayData():
    dto = dict()
    # 支付宝的店铺编号
    dto["alipay_store_id"] = ""
    # 订单包含的商品列表信息
    # dto["goods_detail"] = getGoodsDetail()
    # 业务扩展参数
    # dto["extend_params"] = getExtendParams()
    # 商户操作员编号
    # dto["operator_id"] = ""
    # 商户门店编号
    dto["store_id"] = ""
    # 外部指定买家
    # dto["ext_user_info"] = getExtUserInfo()

    return json.dumps(dto)

def getExtUserInfo():
    dto = dict()
    # 姓名
    # dto["name"] = ""
    # 手机号
    # dto["mobile"] = ""
    # 证件类型
    # dto["cert_type"] = ""
    # 证件号
    # dto["cert_no"] = ""
    # 允许的最小买家年龄
    # dto["min_age"] = ""
    # 是否强制校验付款人身份信息
    # dto["fix_buyer"] = ""
    # 是否强制校验身份信息
    # dto["need_check_info"] = ""

    return dto;

def getExtendParams():
    dto = dict()
    # 卡类型
    # dto["card_type"] = ""
    # 支付宝点餐场景类型
    # dto["food_order_type"] = ""
    # 花呗分期数
    # dto["hb_fq_num"] = ""
    # 花呗卖家承担的手续费百分比
    # dto["hb_fq_seller_percent"] = ""
    # 行业数据回流信息
    # dto["industry_reflux_info"] = ""
    # 停车场id
    # dto["parking_id"] = ""
    # 系统商编号
    # dto["sys_service_provider_id"] = ""

    return dto;

def getGoodsDetail():
    dto = dict()
    # 商品的编号
    # dto["goods_id"] = "test"
    # 商品名称
    # dto["goods_name"] = "test"
    # 商品数量
    # dto["quantity"] = "test"
    # 商品单价
    # dto["price"] = "test"
    # 商品类目树
    # dto["categories_tree"] = ""
    # 商品类目
    # dto["goods_category"] = ""
    # 商品描述信息
    # dto["body"] = ""
    # 商品的展示地址
    # dto["show_url"] = ""

    dtoList = [dto]
    return dtoList

def getWxData():
    dto = dict()
    # 收款设备IP直联模式必填字段；&lt;font color&#x3D;&quot;green&quot;&gt;示例值：192.168.2.2&lt;/font&gt;
    # dto["spbill_create_ip"] = "test"
    # 子商户公众账号id
    # dto["sub_appid"] = ""
    # 用户标识
    # dto["openid"] = ""
    # 子商户用户标识
    # dto["sub_openid"] = ""
    # 设备号
    # dto["device_info"] = ""
    # 附加数据
    # dto["attach"] = ""
    # 商品详情
    # dto["detail"] = getDetail()
    # 场景信息
    # dto["scene_info"] = getSceneInfo()
    # 单品优惠标识
    # dto["promotion_flag"] = ""
    # 电子发票入口开放标识
    # dto["receipt"] = ""

    return json.dumps(dto)

def getSceneInfo():
    dto = dict()
    # 门店信息
    # dto["store_info"] = getStoreInfo()

    return dto;

def getStoreInfo():
    dto = dict()
    # 门店id
    # dto["id"] = ""
    # 门店名称
    # dto["name"] = ""
    # 门店行政区划码
    # dto["area_code"] = ""
    # 门店详细地址
    # dto["address"] = ""

    dtoList = [dto]
    return dtoList

def getDetail():
    dto = dict()
    # 单品列表
    # dto["goods_detail"] = getGoodsDetailWxRucan()
    # 订单原价
    # dto["cost_price"] = ""
    # 商品小票ID
    # dto["receipt_id"] = ""

    return dto;

def getGoodsDetailWxRucan():
    dto = dict()
    # 商品编码
    # dto["goods_id"] = "test"
    # 商品数量
    # dto["quantity"] = "test"
    # 商品名称
    # dto["goods_name"] = ""
    # 商品单价
    # dto["price"] = ""
    # 微信侧商品编码
    # dto["wxpay_goods_id"] = ""

    dtoList = [dto]
    return dtoList

def getAcctSplitBunch():
    dto = dict()
    # 分账明细
    # dto["acct_infos"] = getAcctInfosRucan()

    return json.dumps(dto)

def getAcctInfosRucan():
    dto = dict()
    # 分账金额
    # dto["div_amt"] = "test"
    # 被分账方ID
    # dto["huifu_id"] = "test"
    # 账户号
    # dto["acct_id"] = ""

    dtoList = [dto]
    return dtoList

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


def build_extend_infos():
    """
    非必填字段

    :return: 非必填字段组成的字典
    """
    extend_infos = dict()
    # 交易有效期
    extend_infos["time_expire"] = "20220918150330"
    # 手续费扣款标志
    # extend_infos["fee_flag"] = ""
    # 禁用支付方式
    extend_infos["limit_pay_type"] = ""
    # 是否延迟交易
    extend_infos["delay_acct_flag"] = "Y"
    # 渠道号
    extend_infos["channel_no"] = ""
    # 补贴支付信息
    # extend_infos["combinedpay_data"] = getCombinedpayData()
    # 场景类型
    extend_infos["pay_scene"] = ""
    # 分账对象
    # extend_infos["acct_split_bunch"] = getAcctSplitBunch()
    # 传入分帐遇到优惠的处理规则
    extend_infos["term_div_coupon_type"] = "3"
    # 聚合反扫微信参数集合
    # extend_infos["wx_data"] = getWxData()
    # 支付宝扩展参数集合
    extend_infos["alipay_data"] = getAlipayData()
    # 银联参数集合
    # extend_infos["unionpay_data"] = getUnionpayData()
    # 设备信息
    extend_infos["terminal_device_info"] = getTerminalDeviceInfo()
    # 异步通知地址
    extend_infos["notify_url"] = "http://www.baidu.com"
    # 交易备注
    extend_infos["remark"] = ""
    # 账户号
    # extend_infos["acct_id"] = ""
    return extend_infos


class TestV2TradePaymentMicropayRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 聚合反扫接口 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2TradePaymentMicropayRequest()
        request.req_date = ""
        request.req_seq_id = ""
        request.huifu_id = "6666000018328947"
        request.trans_amt = "0.01"
        request.goods_desc = "聚合反扫消费"
        request.auth_code = "2884138408701518074"
        request.risk_check_data = getRiskCheckData()

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""