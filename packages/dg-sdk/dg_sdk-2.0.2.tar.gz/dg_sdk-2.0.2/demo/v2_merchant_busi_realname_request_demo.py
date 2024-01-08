import unittest
import dg_sdk
import json
from demo.demo_config import *


def getSpecialFileInfoList():
    dto = dict()
    # 文件类型
    dto["file_type"] = "F33"
    # 文件jfileID
    dto["file_id"] = "49ac7d9b-851c-31b4-8b21-2983ea97b98c"

    dtoList = [dto]
    return json.dumps(dtoList)

def getUboInfoList():
    dto = dict()
    # 受益人证件类型
    dto["ubo_id_doc_type"] = "00"
    # 证件正面照片
    dto["ubo_id_doc_copy"] = "c7faf0e6-39e9-3c35-9075-2312ad6f4ea4"
    # 受益人证件姓名
    dto["ubo_id_doc_name"] = "杨雷"
    # 受益人证件号码
    dto["ubo_id_doc_number"] = "110101199003072631"
    # 证件居住地址
    dto["ubo_id_doc_address"] = "上海市徐汇区宜山路789号"
    # 证件有效期开始时间
    dto["ubo_period_begin"] = "19900307"
    # 证件有效期结束时间
    dto["ubo_period_end"] = "长期"
    # 证件反面照片
    dto["ubo_id_doc_copy_back"] = "c7faf0e6-39e9-3c35-9075-2312ad6f4ea4"

    dtoList = [dto]
    return json.dumps(dtoList)


def build_extend_infos():
    """
    非必填字段

    :return: 非必填字段组成的字典
    """
    extend_infos = dict()
    # 子渠道号
    extend_infos["pay_channel_id"] = "JP00001"
    # 支付场景
    extend_infos["pay_scene"] = "01"
    # 经营者/法人是否为受益人
    extend_infos["owner"] = "N"
    # 法人证件居住地址
    extend_infos["identification_address"] = "上海市徐汇区宜山路789号789室"
    # 受益人信息
    extend_infos["ubo_info_list"] = getUboInfoList()
    # 联系人证件类型
    extend_infos["contact_id_doc_type"] = "01"
    # 联系人证件有效期开始时间
    extend_infos["contact_period_begin"] = "1990-03-07"
    # 联系人证件有效期结束时间
    extend_infos["contact_period_end"] = "长期"
    # 证书类型
    extend_infos["cert_type"] = "CERTIFICATE_TYPE_2389"
    # 证书编号
    extend_infos["cert_number"] = "1234567892"
    # 证书照片
    extend_infos["cert_copy"] = ""
    # 小微经营类型
    extend_infos["micro_biz_type"] = ""
    # 门店名称
    extend_infos["store_name"] = ""
    # 门店门头照片
    extend_infos["store_header_copy"] = ""
    # 店内环境照片
    extend_infos["store_indoor_copy"] = ""
    # 门店省市编码
    extend_infos["store_address_code"] = ""
    # 门店地址
    extend_infos["store_address"] = ""
    # 身份证件正面照片
    extend_infos["identification_front_copy"] = "c7faf0e6-39e9-3c35-9075-2312ad6f4ea4"
    # 身份证件反面照片
    extend_infos["identification_back_copy"] = "c7faf0e6-39e9-3c35-9075-2312ad6f4ea4"
    # 单位证明函照片
    extend_infos["company_prove_copy"] = ""
    # 是否金融机构
    extend_infos["finance_institution_flag"] = "N"
    # 金融机构类型
    extend_infos["finance_type"] = ""
    # 特殊行业Id
    extend_infos["category_id"] = ""
    # 文件列表
    extend_infos["special_file_info_list"] = getSpecialFileInfoList()
    return extend_infos


class TestV2MerchantBusiRealnameRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 微信实名认证 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2MerchantBusiRealnameRequest()
        request.req_seq_id = ""
        request.req_date = ""
        request.huifu_id = "6666000104854510"
        request.name = "小枫"
        request.mobile = "17521205027"
        request.id_card_number = "130224198806083798"
        request.contact_type = "SUPER"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""