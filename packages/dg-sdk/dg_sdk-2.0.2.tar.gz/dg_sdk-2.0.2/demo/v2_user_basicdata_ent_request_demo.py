import unittest
import dg_sdk
import json
from demo.demo_config import *


def getFileList():
    dto = dict()
    # 文件类型
    # dto["file_type"] = "test"
    # 文件jfileID
    # dto["file_id"] = "test"
    # 文件名称
    # dto["file_name"] = ""

    dtoList = [dto]
    return json.dumps(dtoList)


def build_extend_infos():
    """
    非必填字段

    :return: 非必填字段组成的字典
    """
    extend_infos = dict()
    # 经营简称
    extend_infos["short_name"] = "企业商户"
    # 联系人电子邮箱
    extend_infos["contact_email"] = "jeff.peng@huifu.com"
    # 管理员账号
    extend_infos["login_name"] = "Lg2022022201374721361"
    # 操作员
    extend_infos["operator_id"] = ""
    # 是否发送短信标识
    extend_infos["sms_send_flag"] = "1"
    # 扩展方字段
    extend_infos["expand_id"] = ""
    # 文件列表
    # extend_infos["file_list"] = getFileList()
    # 公司类型
    # extend_infos["ent_type"] = ""
    return extend_infos


class TestV2UserBasicdataEntRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 企业用户基本信息开户 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2UserBasicdataEntRequest()
        request.req_seq_id = ""
        request.req_date = ""
        request.reg_name = "企业商户名称8225"
        request.license_code = "20220222013747149"
        request.license_validity_type = "1"
        request.license_begin_date = "20200117"
        request.license_end_date = "20400117"
        request.reg_prov_id = "310000"
        request.reg_area_id = "310100"
        request.reg_district_id = "310104"
        request.reg_detail = "上海市宜山路"
        request.legal_name = "陈立五"
        request.legal_cert_type = "00"
        request.legal_cert_no = "321084198912066582"
        request.legal_cert_validity_type = "1"
        request.legal_cert_begin_date = "20120801"
        request.legal_cert_end_date = "20300801"
        request.contact_name = "小的"
        request.contact_mobile = "13764462211"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""