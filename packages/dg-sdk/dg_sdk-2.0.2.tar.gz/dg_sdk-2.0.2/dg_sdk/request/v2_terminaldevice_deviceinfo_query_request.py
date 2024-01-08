from dg_sdk.core.request_tools import request_post
from dg_sdk.request.request_api_urls import V2_TERMINALDEVICE_DEVICEINFO_QUERY



class V2TerminaldeviceDeviceinfoQueryRequest(object):
    """
    绑定终端信息查询
    """

    # 请求流水号
    req_seq_id = ""
    # 请求时间
    req_date = ""
    # 汇付客户Id
    huifu_id = ""
    # 分页大小
    page_size = ""
    # 当前页码
    page_num = ""

    def post(self, extend_infos):
        """
        绑定终端信息查询

        :param extend_infos: 扩展字段字典
        :return:
        """

        required_params = {
            "req_seq_id":self.req_seq_id,
            "req_date":self.req_date,
            "huifu_id":self.huifu_id,
            "page_size":self.page_size,
            "page_num":self.page_num
        }
        required_params.update(extend_infos)
        return request_post(V2_TERMINALDEVICE_DEVICEINFO_QUERY, required_params)
