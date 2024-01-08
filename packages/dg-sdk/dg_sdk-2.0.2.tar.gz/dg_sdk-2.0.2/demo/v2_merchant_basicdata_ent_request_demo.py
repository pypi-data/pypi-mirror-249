import unittest
import dg_sdk
import json
from demo.demo_config import *


def getSignUserInfo():
    dto = dict()
    # 签约人类型
    # dto["type"] = "test"
    # 姓名
    # dto["name"] = ""
    # 手机号
    # dto["mobile_no"] = ""
    # 身份证
    # dto["cert_no"] = ""
    # 身份证照片-人像面
    # dto["identity_front_file_id"] = ""
    # 身份证照片-国徽面
    # dto["identity_back_file_id"] = ""
    # 法人授权书
    # dto["auth_file_id"] = ""

    return json.dumps(dto)

def getSettleConfig():
    dto = dict()
    # 结算周期
    dto["settle_cycle"] = "D1"
    # 结算手续费外扣商户号填写承担手续费的汇付商户号；当out_settle_flag&#x3D;1时必填，否则非必填；&lt;font color&#x3D;&quot;green&quot;&gt;示例值：6666000123123123&lt;/font&gt;
    dto["out_settle_huifuid"] = ""
    # 起结金额
    dto["min_amt"] = "1.00"
    # 留存金额
    dto["remained_amt"] = "2.00"
    # 结算摘要
    dto["settle_abstract"] = "abstract"
    # 手续费外扣标记
    dto["out_settle_flag"] = "2"
    # 结算手续费外扣账户类型
    dto["out_settle_acct_type"] = ""
    # 节假日结算手续费率（%）
    dto["fixed_ratio"] = "5.00"
    # 结算方式
    dto["settle_pattern"] = ""
    # 结算批次号
    dto["settle_batch_no"] = ""
    # 是否优先到账
    dto["is_priority_receipt"] = ""
    # 自定义结算处理时间
    dto["settle_time"] = ""
    # 节假日结算手续费固定金额（元）
    # dto["constant_amt"] = ""

    return json.dumps(dto)

def getCashConfig():
    dto = dict()
    # 取现固定手续费（元）fix_amt与fee_rate至少填写一项，单位元，需保留小数点后两位，不收费请填写0.00； &lt;font color&#x3D;&quot;green&quot;&gt;示例值：1.00&lt;/font&gt;
    dto["fix_amt"] = "1.00"
    # 取现手续费率（%）fix_amt与fee_rate至少填写一项，单位%，需保留小数点后两位，取值范围[0.00,100.00]，不收费请填写0.00；&lt;font color&#x3D;&quot;green&quot;&gt;示例值：0.05&lt;/font&gt;&lt;br/&gt;注：如果fix_amt与fee_rate都填写了则手续费&#x3D;fix_amt+支付金额*fee_rate
    dto["fee_rate"] = ""
    # 取现类型
    dto["cash_type"] = "D0"
    # 是否交易手续费外扣
    # dto["out_fee_flag"] = ""
    # 手续费承担方
    # dto["out_fee_huifu_id"] = ""
    # 交易手续费外扣的账户类型
    # dto["out_fee_acct_type"] = ""

    dtoList = [dto]
    return json.dumps(dtoList)

def getCardInfo():
    dto = dict()
    # 结算账户类型
    dto["card_type"] = "1"
    # 结算账户名
    dto["card_name"] = "陈立二"
    # 结算账号
    dto["card_no"] = "6225682141000000000"
    # 银行所在省参考[地区编码](https://paas.huifu.com/partners/api/#/csfl/api_csfl_dqbm)；&lt;font color&#x3D;&quot;green&quot;&gt;示例值：310000&lt;/font&gt;；如修改省市要级联修改&lt;br/&gt;当card_type&#x3D;0时非必填， 当card_type&#x3D;1或2时必填
    dto["prov_id"] = "310000"
    # 银行所在市参考[地区编码](https://paas.huifu.com/partners/api/#/csfl/api_csfl_dqbm)；&lt;font color&#x3D;&quot;green&quot;&gt;示例值：310100&lt;/font&gt;；如修改省市要级联修改&lt;br/&gt;当card_type&#x3D;0时非必填， 当card_type&#x3D;1或2时必填
    dto["area_id"] = "310100"
    # 联行号参考：[银行支行编码](https://paas.huifu.com/partners/api/#/csfl/api_csfl_yhzhbm) 当card_type&#x3D;0时必填， 当card_type&#x3D;1或2时非必填 &lt;br/&gt;&lt;font color&#x3D;&quot;green&quot;&gt;示例值：102290026507&lt;/font&gt;
    dto["branch_code"] = "103290040169"
    # 持卡人证件类型持卡人证件类型，参见《[自然人证件类型](https://paas.huifu.com/partners/api/#/api_ggcsbm?id&#x3D;%e8%87%aa%e7%84%b6%e4%ba%ba%e8%af%81%e4%bb%b6%e7%b1%bb%e5%9e%8b)》。&lt;br/&gt; 当card_type&#x3D;0时为空， 当card_type&#x3D;1或2时必填； &lt;font color&#x3D;&quot;green&quot;&gt;示例值：00&lt;/font&gt;
    dto["cert_type"] = "00"
    # 持卡人证件有效期截止日期日期格式：yyyyMMdd，以北京时间为准。&lt;font color&#x3D;&quot;green&quot;&gt;示例值：20220125&lt;/font&gt;&lt;br/&gt;  当cert_validity_type&#x3D;0时必填；当cert_validity_type&#x3D;1时为空
    dto["cert_end_date"] = "20301201"
    # 银行编码
    dto["bank_code"] = "01030000"
    # 支行名称
    dto["branch_name"] = "中国农业银行股份有限公司上海马当路支行"
    # 持卡人证件号码
    dto["cert_no"] = "321084198912066000"
    # 持卡人证件有效期类型
    dto["cert_validity_type"] = "1"
    # 持卡人证件有效期开始日期
    dto["cert_begin_date"] = "20121201"
    # 结算人手机号
    dto["mp"] = "13700000000"

    return json.dumps(dto)


def build_extend_infos():
    """
    非必填字段

    :return: 非必填字段组成的字典
    """
    extend_infos = dict()
    # 营业执照类型
    extend_infos["license_type"] = ""
    # 商户通知标识
    extend_infos["sms_send_flag"] = "Y"
    # 管理员账号
    extend_infos["login_name"] = "LG20220422267883697"
    # 取现信息配置
    extend_infos["cash_config"] = getCashConfig()
    # 结算规则配置
    extend_infos["settle_config"] = getSettleConfig()
    # 异步请求地址
    extend_infos["async_return_url"] = "virgo://http://192.168.85.157:30031/sspm/testVirgo"
    # D1结算协议
    extend_infos["settle_agree_pic"] = ""
    # 商户英文名称
    extend_infos["mer_en_name"] = ""
    # 商户主页URL
    extend_infos["mer_url"] = ""
    # 商户ICP备案编号
    extend_infos["mer_icp"] = ""
    # 签约人
    # extend_infos["sign_user_info"] = getSignUserInfo()
    # 是否总部商户
    # extend_infos["head_office_flag"] = ""
    # 使用总部资料
    # extend_infos["use_head_info_flag"] = ""
    # 开户许可证
    # extend_infos["reg_acct_pic"] = ""
    # 结算卡正面
    # extend_infos["settle_card_front_pic"] = ""
    # 结算卡反面
    # extend_infos["settle_card_back_pic"] = ""
    # 结算人身份证国徽面
    # extend_infos["settle_cert_back_pic"] = ""
    # 结算人身份证人像面
    # extend_infos["settle_cert_front_pic"] = ""
    # 税务登记证
    # extend_infos["tax_reg_pic"] = ""
    # 法人身份证国徽面
    # extend_infos["legal_cert_back_pic"] = ""
    # 法人身份证人像面
    # extend_infos["legal_cert_front_pic"] = ""
    # 营业执照图片
    # extend_infos["license_pic"] = ""
    # 授权委托书
    # extend_infos["auth_enturst_pic"] = ""
    # 组织机构代码证
    # extend_infos["org_code_pic"] = ""
    return extend_infos


class TestV2MerchantBasicdataEntRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 企业商户基本信息入驻(2022) - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2MerchantBasicdataEntRequest()
        request.req_seq_id = ""
        request.req_date = ""
        request.upper_huifu_id = "6666000003080000"
        request.reg_name = "集成企业商户8664"
        request.short_name = "企业商户3471"
        request.ent_type = "1"
        request.license_code = "20220422267883697"
        request.license_validity_type = "1"
        request.license_begin_date = "20200401"
        request.license_end_date = ""
        request.reg_prov_id = "350000"
        request.reg_area_id = "350200"
        request.reg_district_id = "350203"
        request.reg_detail = "吉林省长春市思明区解放2路59096852"
        request.legal_name = "陈立二"
        request.legal_cert_type = "00"
        request.legal_cert_no = "321084198912060000"
        request.legal_cert_validity_type = "1"
        request.legal_cert_begin_date = "20121201"
        request.legal_cert_end_date = "20301201"
        request.prov_id = "310000"
        request.area_id = "310100"
        request.district_id = "310104"
        request.detail_addr = "吉林省长春市思明区解放1路49227677"
        request.contact_name = "联系人"
        request.contact_mobile_no = "13111112222"
        request.contact_email = "jeff.peng@huifu.com"
        request.service_phone = "021-121111221"
        request.busi_type = "1"
        request.receipt_name = "盈盈超市"
        request.mcc = "5411"
        request.card_info = getCardInfo()
        request.open_licence_no = ""
        request.head_huifu_id = "test"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""