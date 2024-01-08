import unittest
import dg_sdk
import json
from demo.demo_config import *


def getFileList():
    dto = dict()
    # 文件类型
    dto["file_type"] = "F01"
    # 文件jfileID
    dto["file_id"] = "71da066c-5d15-3658-a86d-4e85ee67808a"
    # 文件名称
    dto["file_name"] = "企业营业执照1.jpg"

    dtoList = [dto]
    return json.dumps(dtoList)


def build_extend_infos():
    """
    非必填字段

    :return: 非必填字段组成的字典
    """
    extend_infos = dict()
    # 企业用户名称
    # extend_infos["reg_name"] = ""
    # 经营简称
    extend_infos["short_name"] = "企业商户测试22"
    # 公司类型
    # extend_infos["ent_type"] = ""
    # 法人姓名
    extend_infos["legal_name"] = "陈立一"
    # 法人证件类型
    extend_infos["legal_cert_type"] = "00"
    # 法人证件号码
    extend_infos["legal_cert_no"] = "370684198903061000"
    # 法人证件有效期类型
    extend_infos["legal_cert_validity_type"] = "0"
    # 法人证件有效期开始日期
    extend_infos["legal_cert_begin_date"] = "20121010"
    # 法人证件有效期截止日期
    extend_infos["legal_cert_end_date"] = "20301010"
    # 联系人姓名
    extend_infos["contact_name"] = "花朵"
    # 联系人电子邮箱
    extend_infos["contact_email"] = "chang@huifu.com"
    # 联系人手机号
    extend_infos["contact_mobile"] = "13764462000"
    # 证照有效期类型
    extend_infos["license_validity_type"] = "1"
    # 证照有效期起始日期
    extend_infos["license_begin_date"] = "20200117"
    # 证照有效期结束日期
    extend_infos["license_end_date"] = "20400117"
    # 注册地址(省)
    extend_infos["reg_prov_id"] = "310000"
    # 注册地址(市)
    extend_infos["reg_area_id"] = "310100"
    # 注册地址(区)
    extend_infos["reg_district_id"] = "310104"
    # 注册地址(详细信息)
    extend_infos["reg_detail"] = "上海市宜山路"
    # 文件列表
    extend_infos["file_list"] = getFileList()
    return extend_infos


class TestV2UserBasicdataEntModifyRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 企业用户基本信息修改 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2UserBasicdataEntModifyRequest()
        request.req_date = ""
        request.req_seq_id = ""
        request.huifu_id = "6666000103862211"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""