from dg_sdk.core.request_tools import request_post
from dg_sdk.request.request_api_urls import V2_USER_BASICDATA_ENT_MODIFY



class V2UserBasicdataEntModifyRequest(object):
    """
    企业用户基本信息修改
    """

    # 请求日期
    req_date = ""
    # 请求流水号
    req_seq_id = ""
    # 汇付客户Id
    huifu_id = ""

    def post(self, extend_infos):
        """
        企业用户基本信息修改

        :param extend_infos: 扩展字段字典
        :return:
        """

        required_params = {
            "req_date":self.req_date,
            "req_seq_id":self.req_seq_id,
            "huifu_id":self.huifu_id
        }
        required_params.update(extend_infos)
        return request_post(V2_USER_BASICDATA_ENT_MODIFY, required_params)
