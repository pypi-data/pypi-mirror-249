import unittest
import dg_sdk
import json
from demo.demo_config import *


def getTerminalInfoList():
    dto = dict()
    # 终端硬件序列号
    dto["sn"] = "433333"
    # 终端21号文编号
    dto["tusn"] = "J434445679"
    # 终端型号代号
    dto["dev_model_code"] = "01"
    # 终端布放地址
    dto["terminal_address"] = "上海额的发"

    dtoList = [dto]
    return json.dumps(dtoList)


def build_extend_infos():
    """
    非必填字段

    :return: 非必填字段组成的字典
    """
    extend_infos = dict()
    # 终端信息
    extend_infos["terminal_info_list"] = getTerminalInfoList()
    return extend_infos


class TestV2TerminaldeviceDeviceinfoAddRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 新增终端报备 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2TerminaldeviceDeviceinfoAddRequest()
        request.req_seq_id = ""
        request.req_date = ""
        request.huifu_id = "6666000104575213"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""