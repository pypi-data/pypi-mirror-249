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
    # 个人证件有效期类型
    extend_infos["cert_validity_type"] = "2"
    # 个人证件有效期开始日期
    extend_infos["cert_begin_date"] = "20200111"
    # 个人证件有效期截止日期
    extend_infos["cert_end_date"] = "20400111"
    # 电子邮箱
    extend_infos["email"] = "jeff.peng@huifu.com"
    # 手机号
    extend_infos["mobile_no"] = "15556622000"
    # 文件列表
    # extend_infos["file_list"] = getFileList()
    return extend_infos


class TestV2UserBasicdataIndvModifyRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 个人用户基本信息修改 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2UserBasicdataIndvModifyRequest()
        request.req_seq_id = ""
        request.req_date = ""
        request.huifu_id = "6666000103854106"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""