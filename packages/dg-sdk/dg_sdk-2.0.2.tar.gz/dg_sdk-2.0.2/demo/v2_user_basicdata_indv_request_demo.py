import unittest
import dg_sdk
import json
from demo.demo_config import *


def getFileList():
    dto = dict()
    # 文件类型
    dto["file_type"] = "F04"
    # 文件jfileID
    dto["file_id"] = "2022022201394949297117211"
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
    # 个人证件有效期截止日期
    extend_infos["cert_end_date"] = "20400117"
    # 电子邮箱
    extend_infos["email"] = "jeff.peng@huifu.com"
    # 管理员账号
    extend_infos["login_name"] = "Lg2022022201394910571"
    # 是否发送短信标识
    extend_infos["sms_send_flag"] = "1"
    # 拓展方字段
    extend_infos["expand_id"] = ""
    # 文件列表
    extend_infos["file_list"] = getFileList()
    return extend_infos


class TestV2UserBasicdataIndvRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 个人用户基本信息开户 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2UserBasicdataIndvRequest()
        request.req_seq_id = ""
        request.req_date = ""
        request.name = "个人用户名称3657"
        request.cert_type = "00"
        request.cert_no = "321084198912066512"
        request.cert_validity_type = "1"
        request.cert_begin_date = "20200117"
        request.mobile_no = "13764462205"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""