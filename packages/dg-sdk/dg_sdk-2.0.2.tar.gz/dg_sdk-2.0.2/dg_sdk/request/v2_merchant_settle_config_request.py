from dg_sdk.core.request_tools import request_post
from dg_sdk.request.request_api_urls import V2_MERCHANT_SETTLE_CONFIG



class V2MerchantSettleConfigRequest(object):
    """
    子账户开通配置(2022)
    """

    # 请求流水号
    req_seq_id = ""
    # 请求日期
    req_date = ""
    # 商户/用户汇付Id
    huifu_id = ""
    # 上级汇付Id
    upper_huifu_id = ""
    # 子账户类型
    acct_type = ""
    # 账户名称
    acct_name = ""

    def post(self, extend_infos):
        """
        子账户开通配置(2022)

        :param extend_infos: 扩展字段字典
        :return:
        """

        required_params = {
            "req_seq_id":self.req_seq_id,
            "req_date":self.req_date,
            "huifu_id":self.huifu_id,
            "upper_huifu_id":self.upper_huifu_id,
            "acct_type":self.acct_type,
            "acct_name":self.acct_name
        }
        required_params.update(extend_infos)
        return request_post(V2_MERCHANT_SETTLE_CONFIG, required_params)
