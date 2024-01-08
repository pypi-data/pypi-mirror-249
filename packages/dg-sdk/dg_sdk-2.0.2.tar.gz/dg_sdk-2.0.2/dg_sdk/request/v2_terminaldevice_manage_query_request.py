from dg_sdk.core.request_tools import request_post
from dg_sdk.request.request_api_urls import V2_TERMINALDEVICE_MANAGE_QUERY



class V2TerminaldeviceManageQueryRequest(object):
    """
    服务商终端列表查询
    """

    # 请求流水号
    req_seq_id = ""
    # 请求时间
    req_date = ""

    def post(self, extend_infos):
        """
        服务商终端列表查询

        :param extend_infos: 扩展字段字典
        :return:
        """

        required_params = {
            "req_seq_id":self.req_seq_id,
            "req_date":self.req_date
        }
        required_params.update(extend_infos)
        return request_post(V2_TERMINALDEVICE_MANAGE_QUERY, required_params)
