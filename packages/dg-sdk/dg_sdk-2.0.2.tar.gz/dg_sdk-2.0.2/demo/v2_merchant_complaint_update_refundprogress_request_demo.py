import unittest
import dg_sdk
import json
from demo.demo_config import *


def getFileInfo():
    dto = dict()
    # 拒绝退款的举证图片1
    dto["reject_media_pic1"] = "a8a096a3-0dd4-3b0e-886c-9afb20d23b1a"
    # 拒绝退款的举证图片2
    dto["reject_media_pic2"] = "a8a096a3-0dd4-3b0e-886c-9afb20d23b2a"
    # 拒绝退款的举证图片3
    dto["reject_media_pic3"] = "a8a096a3-0dd4-3b0e-886c-9afb20d23b3a"
    # 拒绝退款的举证图片4
    dto["reject_media_pic4"] = "a8a096a3-0dd4-3b0e-886c-9afb20d23b4a"

    return json.dumps(dto)


def build_extend_infos():
    """
    非必填字段

    :return: 非必填字段组成的字典
    """
    extend_infos = dict()
    # 预计发起退款时间
    extend_infos["launch_refund_day"] = ""
    # 拒绝退款原因
    extend_infos["reject_reason"] = ""
    # 备注
    extend_infos["remark"] = "我是备注1111101"
    # 文件列表
    extend_infos["file_info"] = getFileInfo()
    return extend_infos


class TestV2MerchantComplaintUpdateRefundprogressRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 更新退款审批结果 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2MerchantComplaintUpdateRefundprogressRequest()
        request.req_seq_id = ""
        request.req_date = ""
        request.complaint_id = "200000020221020220032600930"
        request.action = "APPROVE"
        request.mch_id = "1502074862"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""