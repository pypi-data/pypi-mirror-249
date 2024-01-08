from dg_sdk.core.request_tools import request_post
from dg_sdk.request.request_api_urls import V2_TRADE_ACCTPAYMENT_PAY



class V2TradeAcctpaymentPayRequest(object):
    """
    余额支付
    """

    # 请求流水号
    req_seq_id = ""
    # 请求日期
    req_date = ""
    # 出款方商户号
    out_huifu_id = ""
    # 支付金额
    ord_amt = ""
    # 分账对象
    acct_split_bunch = ""
    # 安全信息
    risk_check_data = ""

    def post(self, extend_infos):
        """
        余额支付

        :param extend_infos: 扩展字段字典
        :return:
        """

        required_params = {
            "req_seq_id":self.req_seq_id,
            "req_date":self.req_date,
            "out_huifu_id":self.out_huifu_id,
            "ord_amt":self.ord_amt,
            "acct_split_bunch":self.acct_split_bunch,
            "risk_check_data":self.risk_check_data
        }
        required_params.update(extend_infos)
        return request_post(V2_TRADE_ACCTPAYMENT_PAY, required_params)
