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
    # 支行名
    extend_infos["subbranch_bank_name"] = "subbranchBankName"
    # 收款方三证合一码
    extend_infos["bank_acct_three_in_one"] = "dfa"
    # 异步通知地址
    extend_infos["notify_url"] = "http://www.gangcai.com"
    return extend_infos


class TestV2TradeSettlementSurrogateRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 银行卡代发 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2TradeSettlementSurrogateRequest()
        request.req_seq_id = ""
        request.req_date = ""
        request.huifu_id = "6666000000041651"
        request.cash_amt = "9.00"
        request.purpose_desc = "v2测试用"
        request.province = "0278"
        request.area = "2619"
        request.bank_code = "01020000"
        request.correspondent_code = "correspondentCode"
        request.bank_account_name = "王大锤"
        request.card_acct_type = "E"
        request.bank_card_no_crypt = "fM3G4fV8dfyA9GvSPckj7DM/0ZPgIuTrCj5chjRP2np/j+5xBkDp+hGLSskALgMijL837blhwVwfpPstkR2t+0aLtRLC1IpggVKKbNefoqcahF2a4zh+YssAulOoQ6T7DDWTjaa0qzILmLV+J/CCW6ioE+pdsBlGKee7Cc0iD6VqAjkSmnx2kWadz9CpaH8ayvyivdkc87SHsSgexQ5scyZdkGYSpXtRf/rSTcfsf5Q3NP+uKA6lJ0hnESiCw/1POoszJrSlGT2U7jpQLDWVENKcW06bReKxQuAdxFaX4DqkwbQeN5nzHvYh14IU8KrZZDAoiCx12x+IcHIVB2tBmw=="
        request.certificate_no_crypt = "cw8BlH40+weHiFnIonCiSak1wWeCiRWpMF1cBHhuE+vagzKT37MRvouVboLnaWwIry3joQOoVJipDTPpzAMGVrbLQTdtZoHhgyynnD3MS0NTPch2W4i9dO3/ikLylbs2HitUlCThXEX7DIrIbLLYZ7zzeYUyXAs6dKlehMNxAaF4utJpxV84tB3ZmCKKFairE6+al4Id+/c7536G0j5lKn7lWSawl8A1UEbMMmHFvydGEBgaCAmvu0WEx7llhtPl1GpJnwqieAt9u+lM0cjUGEYfw54/JnmEF3uVuHqjco/EAMKmWiqONqCT4ptBLlOiT15FUejK0iFiUrS0Y3ytMg=="
        request.certificate_type = "01"
        request.mobile_no_crypt = "Uc2rjt3iqQMIjUubLKvrE4ynG2XoZDXl4sSqHB7xFvz6EyhS+WMm+tp7WLzG97PqdsmlfURRLjmSR3u98Zz0HV7wO4zvUwdOMzA1rX2Ab9Cz6eKHBWwkRpEn8zmq3KdsHpifKd5y6/MuEyXJ6tdKjBrmXTn3Ut6goz+yhUcPbvV4HEMCybRmF9YTvblb7Yk8trMHjOkq6J6EIEfQL3X07WTNpseCtuYF/j5tNws4boezEmOnS2hNkneMR+OfRaZ6UndFAMHd/Lj9fY2mscpPnWNACtmsD2nh0Z8ziwzCYnYAH2EV988cSq2vi3fkgCtd5b8zNGp+XJBefPaK7Vcp+w=="
        request.into_acct_date_type = "T0"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""