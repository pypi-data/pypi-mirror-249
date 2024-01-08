from dg_sdk.core.request_tools import request_post
from dg_sdk.request.request_api_urls import V2_TRADE_ONLINEPAYMENT_TRANSFER_BANKMISTAKE_APPLY



class V2TradeOnlinepaymentTransferBankmistakeApplyRequest(object):
    """
    银行大额转账差错申请
    """

    # 请求流水号
    req_seq_id = ""
    # 请求日期
    req_date = ""
    # 商户号
    huifu_id = ""
    # 交易金额
    trans_amt = ""
    # 订单类型
    order_type = ""
    # 原请求流水号
    org_req_seq_id = ""
    # 原请求日期
    org_req_date = ""
    # 实际打款日期
    remit_date = ""
    # 实际付款方姓名
    certificate_name = ""
    # 实际付款方银行卡号
    bank_card_no = ""
    # 实际付款方银行名称
    bank_name = ""
    # 异步通知地址
    notify_url = ""
    # 商品描述
    goods_desc = ""
    # 汇款凭证文件内容
    certificate_content = ""

    def post(self, extend_infos):
        """
        银行大额转账差错申请

        :param extend_infos: 扩展字段字典
        :return:
        """

        required_params = {
            "req_seq_id":self.req_seq_id,
            "req_date":self.req_date,
            "huifu_id":self.huifu_id,
            "trans_amt":self.trans_amt,
            "order_type":self.order_type,
            "org_req_seq_id":self.org_req_seq_id,
            "org_req_date":self.org_req_date,
            "remit_date":self.remit_date,
            "certificate_name":self.certificate_name,
            "bank_card_no":self.bank_card_no,
            "bank_name":self.bank_name,
            "notify_url":self.notify_url,
            "goods_desc":self.goods_desc,
            "certificate_content":self.certificate_content
        }
        required_params.update(extend_infos)
        return request_post(V2_TRADE_ONLINEPAYMENT_TRANSFER_BANKMISTAKE_APPLY, required_params)
