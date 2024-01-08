from dg_sdk.core.request_tools import request_post
from dg_sdk.request.request_api_urls import V2_USER_BUSI_MODIFY



class V2UserBusiModifyRequest(object):
    """
    用户业务入驻修改
    """

    # 请求流水号
    req_seq_id = ""
    # 请求日期
    req_date = ""
    # 渠道商汇付Id
    upper_huifu_id = ""
    # 汇付ID
    huifu_id = ""

    def post(self, extend_infos):
        """
        用户业务入驻修改

        :param extend_infos: 扩展字段字典
        :return:
        """

        required_params = {
            "req_seq_id":self.req_seq_id,
            "req_date":self.req_date,
            "upper_huifu_id":self.upper_huifu_id,
            "huifu_id":self.huifu_id
        }
        required_params.update(extend_infos)
        return request_post(V2_USER_BUSI_MODIFY, required_params)
