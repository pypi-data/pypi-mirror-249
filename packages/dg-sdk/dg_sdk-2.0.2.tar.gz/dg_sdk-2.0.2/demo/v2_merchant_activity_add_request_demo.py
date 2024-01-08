import unittest
import dg_sdk
import json
from demo.demo_config import *


def getBankAccount():
    dto = dict()
    # 账户名
    dto["card_name"] = "张三"
    # 银行账号
    dto["card_no"] = "6228480402637874213"
    # 开户行名称
    dto["bank_branch_name"] = "招商银行"

    return json.dumps(dto)


def build_extend_infos():
    """
    非必填字段

    :return: 非必填字段组成的字典
    """
    extend_infos = dict()
    # 活动类型
    extend_infos["activity_type"] = "BLUE_SEA"
    # 二级商户号
    extend_infos["sub_mer_id"] = "W5503418657189757903"
    # 二级商户名称
    extend_infos["sub_mer_name"] = ""
    # 异步通知地址
    extend_infos["async_return_url"] = "http://192.168.85.157:30031/sspm/testVirgo"
    # 证明文件图片
    extend_infos["certificate_file_photo"] = "42204258-967e-373c-88d2-1afa4c7bb8ef"
    # 收费样本
    extend_infos["charge_sample_photo"] = "42204258-967e-373c-88d2-1afa4c7bb8ef"
    # 照会
    extend_infos["diplomatic_note_photo"] = "42204258-967e-373c-88d2-1afa4c7bb8ef"
    # 事业单位法人证书图片
    extend_infos["inst_org_photo"] = "42204258-967e-373c-88d2-1afa4c7bb8ef"
    # 法人身份证图片
    extend_infos["legal_person_photo"] = "42204258-967e-373c-88d2-1afa4c7bb8ef"
    # 法人登记证书图片
    extend_infos["legal_person_reg_photo"] = "42204258-967e-373c-88d2-1afa4c7bb8ef"
    # 医疗执业许可证图片
    extend_infos["medical_license_photo"] = "42204258-967e-373c-88d2-1afa4c7bb8ef"
    # 民办非企业单位登记证书图片
    extend_infos["nonenterprise_photo"] = "42204258-967e-373c-88d2-1afa4c7bb8ef"
    # 组织机构代码证图片
    extend_infos["org_cert_photo"] = "42204258-967e-373c-88d2-1afa4c7bb8ef"
    # 机构资质证明照片
    extend_infos["org_qualifi_photo"] = "42204258-967e-373c-88d2-1afa4c7bb8ef"
    # 办学资质图片
    extend_infos["school_license_photo"] = "42204258-967e-373c-88d2-1afa4c7bb8ef"
    # 门店省市区编码
    extend_infos["shop_add_code"] = "110101"
    # 门店街道名称
    extend_infos["shop_street"] = "门店街道名称"
    # 门店租赁证明
    extend_infos["store_tenancy_proof_photo"] = "42204258-967e-373c-88d2-1afa4c7bb8ef"
    # 合作资质证明
    extend_infos["cooper_certi_photo"] = "42204258-967e-373c-88d2-1afa4c7bb8ef"
    # 优惠费率承诺函
    extend_infos["activity_rate_commit_photo"] = "42204258-967e-373c-88d2-1afa4c7bb8ef"
    # 商户同名银行账户信息
    extend_infos["bank_account"] = getBankAccount()
    # 银行开户证明图片
    extend_infos["bank_account_prove_photo"] = ""
    # 机构银行合作授权函图
    extend_infos["bank_agreement_photo"] = ""
    # 行业编码
    extend_infos["industry_code"] = ""
    # 商户行业资质图片
    extend_infos["industry_photo"] = ""
    # 负责人授权函图片
    extend_infos["legal_person_auth_photo"] = ""
    # 食堂经营相关资质
    # extend_infos["food_qualification_proof"] = ""
    return extend_infos


class TestV2MerchantActivityAddRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 商户活动报名 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2MerchantActivityAddRequest()
        request.req_date = ""
        request.req_seq_id = ""
        request.huifu_id = "6666000103627938"
        request.bl_photo = "42204258-967e-373c-88d2-1afa4c7bb8ef"
        request.dh_photo = "42204258-967e-373c-88d2-1afa4c7bb8ef"
        request.fee_type = "7"
        request.mm_photo = "42204258-967e-373c-88d2-1afa4c7bb8ef"
        request.syt_photo = "42204258-967e-373c-88d2-1afa4c7bb8ef"
        request.pay_way = "W"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""