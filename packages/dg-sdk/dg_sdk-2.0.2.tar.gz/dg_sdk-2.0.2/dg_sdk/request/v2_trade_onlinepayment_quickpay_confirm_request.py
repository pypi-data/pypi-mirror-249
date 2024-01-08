from dg_sdk.core.request_tools import request_post
from dg_sdk.request.request_api_urls import V2_TRADE_ONLINEPAYMENT_QUICKPAY_CONFIRM



class V2TradeOnlinepaymentQuickpayConfirmRequest(object):
    """
    快捷支付确认
    """

    # 请求日期
    req_date = ""
    # 请求流水号
    req_seq_id = ""
    # 商户号
    huifu_id = ""
    # 短信验证码
    sms_code = ""
    # 商品描述
    goods_desc = ""
    # 外部地址
    notify_url = ""

    def post(self, extend_infos):
        """
        快捷支付确认

        :param extend_infos: 扩展字段字典
        :return:
        """

        required_params = {
            "req_date":self.req_date,
            "req_seq_id":self.req_seq_id,
            "huifu_id":self.huifu_id,
            "sms_code":self.sms_code,
            "goods_desc":self.goods_desc,
            "notify_url":self.notify_url
        }
        required_params.update(extend_infos)
        return request_post(V2_TRADE_ONLINEPAYMENT_QUICKPAY_CONFIRM, required_params)
