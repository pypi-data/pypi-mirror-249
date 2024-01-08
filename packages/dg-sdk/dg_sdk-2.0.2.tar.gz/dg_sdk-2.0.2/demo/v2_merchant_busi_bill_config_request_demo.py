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
    # SFTP地址
    # extend_infos["ftp_addr"] = ""
    # SFTP用户名
    # extend_infos["ftp_user"] = ""
    # SFTP密码
    # extend_infos["ftp_pwd"] = ""
    # 包含数据范围
    # extend_infos["include_data_range"] = ""
    return extend_infos


class TestV2MerchantBusiBillConfigRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 交易结算对账文件配置 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2MerchantBusiBillConfigRequest()
        request.req_date = ""
        request.req_seq_id = ""
        request.huifu_id = "6666000121363028"
        request.recon_send_flag = "Y"
        request.file_type = "1,2,3,4"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""