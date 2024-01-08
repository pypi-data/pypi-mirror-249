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
    return extend_infos


class TestV2TradeCardbinQueryRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 卡bin信息查询 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2TradeCardbinQueryRequest()
        request.req_date = ""
        request.req_seq_id = ""
        request.bank_card_no_crypt = "b9LE5RccVVLChrHgo9lvpLB1XIyJlEeETa1APmkRQ35z06zJ8zD7cnqypNSnA8iK3uAYVDJtCfrz1Hqu1qTCdu5eVWkjBYaAUtuy1ZD4HkEkqbY9/z5lN4jdDyF8xlzonfxhxzm3OM1fWRoYl39Te+pW71ag0SSbQGu6yhWzFD9mBllbj2RR5fWm9BZVtJTLmitIO/HZfirXkRiCPHBjosQJm2bCrVSuzxqJgqmB9Cp1ADIB+f7fG1/G8RElkJ5zyqhDyinlB5b2+fy3hoyuPqB44GCSLEeOF8V0C9uMNNVor1DwvPRLYleNSw43lW4mFx4PhWhjKrWg2NPfbe0mkQ=="

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""