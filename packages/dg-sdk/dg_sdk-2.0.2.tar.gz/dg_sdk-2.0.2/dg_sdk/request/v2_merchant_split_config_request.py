from dg_sdk.core.request_tools import request_post
from dg_sdk.request.request_api_urls import V2_MERCHANT_SPLIT_CONFIG



class V2MerchantSplitConfigRequest(object):
    """
    商户分账配置(2022)
    """

    # 请求流水号
    req_seq_id = ""
    # 请求时间
    req_date = ""
    # 商户汇付Id
    huifu_id = ""
    # 分账规则来源
    rule_origin = ""
    # 分账开关
    div_flag = ""
    # 最大分账比例
    apply_ratio = ""
    # 生效类型
    start_type = ""

    def post(self, extend_infos):
        """
        商户分账配置(2022)

        :param extend_infos: 扩展字段字典
        :return:
        """

        required_params = {
            "req_seq_id":self.req_seq_id,
            "req_date":self.req_date,
            "huifu_id":self.huifu_id,
            "rule_origin":self.rule_origin,
            "div_flag":self.div_flag,
            "apply_ratio":self.apply_ratio,
            "start_type":self.start_type
        }
        required_params.update(extend_infos)
        return request_post(V2_MERCHANT_SPLIT_CONFIG, required_params)
