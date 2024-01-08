from dg_sdk.core.request_tools import request_post
from dg_sdk.request.request_api_urls import V2_MERCHANT_BUSI_OPEN



class V2MerchantBusiOpenRequest(object):
    """
    商户业务开通(2022)
    """

    # 请求流水号
    req_seq_id = ""
    # 请求日期
    req_date = ""
    # 汇付客户Id
    huifu_id = ""
    # 上级主体ID
    upper_huifu_id = ""

    def post(self, extend_infos):
        """
        商户业务开通(2022)

        :param extend_infos: 扩展字段字典
        :return:
        """

        required_params = {
            "req_seq_id":self.req_seq_id,
            "req_date":self.req_date,
            "huifu_id":self.huifu_id,
            "upper_huifu_id":self.upper_huifu_id
        }
        required_params.update(extend_infos)
        return request_post(V2_MERCHANT_BUSI_OPEN, required_params)
