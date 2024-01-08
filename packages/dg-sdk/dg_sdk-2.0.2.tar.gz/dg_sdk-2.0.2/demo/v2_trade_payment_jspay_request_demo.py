import unittest
import dg_sdk
import json
from demo.demo_config import *


def getTerminalDeviceData():
    dto = dict()
    # 商户设备类型
    # dto["mer_device_type"] = "test"
    # 汇付机具号
    dto["devs_id"] = "SPINTP357338300264411"
    # 设备类型
    dto["device_type"] = "1"
    # 交易设备IP
    dto["device_ip"] = "10.10.0.1"
    # 交易设备MAC
    dto["device_mac"] = ""
    # 交易设备IMEI
    dto["device_imei"] = ""
    # 交易设备IMSI
    dto["device_imsi"] = ""
    # 交易设备ICCID
    dto["device_icc_id"] = ""
    # 交易设备WIFIMAC
    dto["device_wifi_mac"] = ""
    # 交易设备GPS
    dto["device_gps"] = "192.168.0.0"
    # 商户终端应用程序版本
    # dto["app_version"] = ""
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
    # 商户终端序列号
    # dto["serial_num"] = ""

    return json.dumps(dto)

def getRiskCheckData():
    dto = dict()
    # ip地址
    dto["ip_addr"] = "180.167.105.130"
    # 基站地址
    dto["base_station"] = "192.168.1.1"
    # 纬度
    dto["latitude"] = "33.3"
    # 经度
    dto["longitude"] = "33.3"

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

def getDcData():
    dto = dict()
    # 数字货币银行编号
    # dto["digital_bank_no"] = ""

    return json.dumps(dto)

def getUnionpayData():
    dto = dict()
    # 收款方附加数据
    # dto["acq_addn_data"] = ""
    # 地区信息
    # dto["area_info"] = ""
    # 持卡人ip
    # dto["customer_ip"] = ""
    # 前台通知地址
    # dto["front_url"] = ""
    # 订单描述
    # dto["order_desc"] = ""
    # 收款方附言
    # dto["payee_comments"] = ""
    # 收款方信息
    # dto["payee_info"] = getPayeeInfo()
    # 银联分配的服务商机构标识码
    # dto["pnr_ins_id_cd"] = ""
    # 请求方自定义域
    # dto["req_reserved"] = ""
    # 终端信息
    # dto["term_info"] = ""
    # 云闪付用户标识
    # dto["user_id"] = ""

    return json.dumps(dto)

def getPayeeInfo():
    dto = dict()
    # 商户类别
    # dto["mer_cat_code"] = ""
    # 二级商户代码
    # dto["sub_id"] = ""
    # 二级商户名称
    # dto["sub_name"] = ""
    # 终端号
    # dto["term_id"] = ""

    return dto;

def getAlipayData():
    dto = dict()
    # 买家的支付宝唯一用户号
    dto["buyer_id"] = "20880414938706770000"
    # 支付宝的店铺编号
    dto["alipay_store_id"] = ""
    # 买家支付宝账号
    dto["buyer_logon_id"] = "String"
    # 业务扩展参数
    dto["extend_params"] = getExtendParams()
    # 订单包含的商品列表信息
    dto["goods_detail"] = getGoodsDetail()
    # 商户原始订单号
    dto["merchant_order_no"] = "String"
    # 商户操作员编号
    dto["operator_id"] = "123213213"
    # 销售产品码
    dto["product_code"] = "String"
    # 卖家支付宝用户号
    dto["seller_id"] = "String"
    # 商户门店编号
    dto["store_id"] = ""
    # 外部指定买家
    # dto["ext_user_info"] = getExtUserInfo()
    # 订单标题
    # dto["subject"] = ""
    # 商家门店名称
    # dto["store_name"] = ""

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

def getGoodsDetail():
    dto = dict()
    # 商品的编号
    dto["goods_id"] = "12312321"
    # 商品名称(元)
    dto["goods_name"] = "阿里"
    # 商品单价
    dto["price"] = "0.01"
    # 商品数量
    dto["quantity"] = "20"
    # 商品描述信息
    dto["body"] = ""
    # 商品类目树
    dto["categories_tree"] = "String"
    # 商品类目
    dto["goods_category"] = ""
    # 商品的展示地址
    dto["show_url"] = ""

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
    # 花呗卖家承担的手续费百分比
    dto["hb_fq_seller_percent"] = ""
    # 行业数据回流信息
    dto["industry_reflux_info"] = "String"
    # 停车场id
    dto["parking_id"] = "123wsx"
    # 系统商编号
    dto["sys_service_provider_id"] = "1111111"
    # 信用卡分期资产方式
    # dto["fq_channels"] = ""

    return dto;

def getWxData():
    dto = dict()
    # 子商户公众账号id
    # dto["sub_appid"] = ""
    # 用户标识
    # dto["openid"] = ""
    # 子商户用户标识
    # dto["sub_openid"] = ""
    # 附加数据
    # dto["attach"] = ""
    # 商品描述
    # dto["body"] = ""
    # 商品详情
    # dto["detail"] = getDetail()
    # 设备号
    # dto["device_info"] = ""
    # 订单优惠标记
    # dto["goods_tag"] = ""
    # 实名支付
    # dto["identity"] = ""
    # 开发票入口开放标识
    # dto["receipt"] = ""
    # 场景信息
    # dto["scene_info"] = getSceneInfo()
    # 终端ip
    # dto["spbill_create_ip"] = ""
    # 单品优惠标识
    # dto["promotion_flag"] = ""
    # 新增商品ID
    # dto["product_id"] = ""
    # 指定支付者
    # dto["limit_payer"] = ""

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
    # dto["ass"] = ""

    dtoList = [dto]
    return dtoList

def getDetail():
    dto = dict()
    # 单品列表
    # dto["goods_detail"] = getGoodsDetailWxRucan()
    # 订单原价(元)
    # dto["cost_price"] = ""
    # 商品小票ID
    # dto["receipt_id"] = ""

    return dto;

def getGoodsDetailWxRucan():
    dto = dict()
    # 商品编码
    # dto["goods_id"] = ""
    # 商品名称
    # dto["goods_name"] = ""
    # 商品单价(元)
    # dto["price"] = ""
    # 商品数量
    # dto["quantity"] = ""
    # 微信侧商品编码
    # dto["wxpay_goods_id"] = ""

    dtoList = [dto]
    return dtoList


def build_extend_infos():
    """
    非必填字段

    :return: 非必填字段组成的字典
    """
    extend_infos = dict()
    # 交易有效期
    extend_infos["time_expire"] = "20230418235959"
    # 聚合正扫微信拓展参数集合
    # extend_infos["wx_data"] = getWxData()
    # 支付宝扩展参数集合
    extend_infos["alipay_data"] = getAlipayData()
    # 银联参数集合
    # extend_infos["unionpay_data"] = getUnionpayData()
    # 数字人民币参数集合
    # extend_infos["dc_data"] = getDcData()
    # 分账对象
    extend_infos["acct_split_bunch"] = getAcctSplitBunch()
    # 传入分帐遇到优惠的处理规则
    extend_infos["term_div_coupon_type"] = "0"
    # 补贴支付信息
    # extend_infos["combinedpay_data"] = getCombinedpayData()
    # 账户号
    # extend_infos["acct_id"] = ""
    # 手续费扣款标志
    # extend_infos["fee_flag"] = ""
    # 禁用信用卡标记
    extend_infos["limit_pay_type"] = "NO_CREDIT"
    # 是否延迟交易
    extend_infos["delay_acct_flag"] = "N"
    # 商户贴息标记
    extend_infos["fq_mer_discount_flag"] = "N"
    # 渠道号
    extend_infos["channel_no"] = ""
    # 场景类型
    extend_infos["pay_scene"] = "02"
    # 安全信息
    extend_infos["risk_check_data"] = getRiskCheckData()
    # 设备信息
    extend_infos["terminal_device_data"] = getTerminalDeviceData()
    # 备注
    extend_infos["remark"] = "String"
    # 异步通知地址
    extend_infos["notify_url"] = "http://www.baidu.com"
    return extend_infos


class TestV2TradePaymentJspayRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 聚合正扫接口 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2TradePaymentJspayRequest()
        request.req_date = ""
        request.req_seq_id = ""
        request.huifu_id = "6666000108854952"
        request.goods_desc = "hibs自动化-通用版验证"
        request.trade_type = "A_NATIVE"
        request.trans_amt = "0.10"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""