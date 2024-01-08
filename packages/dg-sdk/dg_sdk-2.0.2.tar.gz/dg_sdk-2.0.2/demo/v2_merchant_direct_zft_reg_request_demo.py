import unittest
import dg_sdk
import json
from demo.demo_config import *



def build_extend_infos():
    """
    非必填字段

    :return: 非必填字段组成的字典
    """
    extend_infos = dict()
    # 渠道商汇付ID
    extend_infos["upper_huifu_id"] = "6666000103521824"
    # 商户别名
    extend_infos["alias_name"] = "哈市盈超市"
    # 法人证件类型
    extend_infos["legal_cert_type"] = "100"
    # 联系人身份证号
    extend_infos["contact_id_card_no"] = "120101199003071300"
    # 联系人电话
    extend_infos["contact_phone"] = "13576266246"
    # 联系人电子邮箱
    extend_infos["contact_email"] = "a066545074@qq.com"
    # 商户站点信息
    extend_infos["zft_site_info_list"] = "[{\"site_type\":\"02\",\"site_url\":\"站点地址\",\"site_name\":\"站点名称\",\"account\":\"\",\"password\":\"测试密码\"}]"
    # 开票资料信息
    extend_infos["zft_invoice_info_list"] = "[{\"auto_invoice_flag\":\"N\",\"accept_electronic_flag\":\"N\",\"tax_payer_qualification\":\"01\",\"title\":\"发票抬头\",\"tax_no\":\"纳税人识别号\",\"tax_payer_valid\":\"20210127\",\"address\":\"开票地址\",\"telephone\":\"10087\",\"bank_account\":\"6228480123456789\",\"mail_name\":\"雷均一\",\"prov_id\":\"310000\",\"area_id\":\"310100\",\"district_id\":\"310104\",\"detail_addr\":\"经营详细地址\",\"mail_telephone\":\"13576266246\",\"bank_name\":\"中国农业银行\"}]"
    # 审核结果异步通知地址
    extend_infos["async_return_url"] = "http://192.168.85.157:30031/sspm/testVirgo"
    return extend_infos


class TestV2MerchantDirectZftRegRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 直付通商户入驻 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2MerchantDirectZftRegRequest()
        request.req_seq_id = ""
        request.req_date = ""
        request.huifu_id = "6666000103521825"
        request.app_id = "2021002122659346"
        request.name = "雷均一"
        request.merchant_type = "0"
        request.mcc = "5331"
        request.cert_type = "100"
        request.cert_no = "120101199003071300"
        request.cert_name = "I_cert_name"
        request.legal_name = "雷均一"
        request.legal_cert_no = "120101199003071300"
        request.service_phone = "10086"
        request.prov_id = "310000"
        request.area_id = "310100"
        request.district_id = "310104"
        request.detail_addr = "上海市徐汇区"
        request.contact_name = "张三"
        request.contact_tag = "02"
        request.contact_type = "LEGAL_PERSON"
        request.contact_mobile_no = "13576266246"
        request.zft_card_info_list = "[{\"card_type\":\"1\",\"card_flag\":\"D\",\"card_name\":\"雷均一\",\"card_no\":\"6228480123456789\",\"prov_id\":\"310000\",\"area_id\":\"310100\",\"bank_code\":\"01030000\",\"bank_name\":\"中国农业银行\",\"branch_code\":\"103290076178\",\"branch_name\":\"中国农业银行股份有限公司上海徐汇支行\"}]"
        request.alipay_logon_id = "13576266246"
        request.industry_qualification_type = ""
        request.service = "2"
        request.sign_time_with_isv = "2021-01-27"
        request.binding_alipay_logon_id = "13576266246"
        request.default_settle_type = "alipayAccount"
        request.file_list = "[{\"file_type\":\"F41\",\"file_id\":\"c679752a-9abc-326d-bb02-8cf770f56d12\",\"file_name\":\"身份证国徽面\"},{\"file_type\":\"F40\",\"file_id\":\"c679752a-9abc-326d-bb02-8cf770f56d12\",\"file_name\":\"身份证人像面\"},{\"file_type\":\"F40\",\"file_id\":\"c679752a-9abc-326d-bb02-8cf770f56d12\",\"file_name\":\"身份证人像面\"}]"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""