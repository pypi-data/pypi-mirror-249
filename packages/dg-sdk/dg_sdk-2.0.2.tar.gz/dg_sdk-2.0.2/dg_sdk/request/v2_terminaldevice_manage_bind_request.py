from dg_sdk.core.request_tools import request_post
from dg_sdk.request.request_api_urls import V2_TERMINALDEVICE_MANAGE_BIND



class V2TerminaldeviceManageBindRequest(object):
    """
    终端绑定
    """

    # 请求流水号
    req_seq_id = ""
    # 请求时间
    req_date = ""
    # 汇付ID
    huifu_id = ""
    # 终端号
    device_id = ""

    def post(self, extend_infos):
        """
        终端绑定

        :param extend_infos: 扩展字段字典
        :return:
        """

        required_params = {
            "req_seq_id":self.req_seq_id,
            "req_date":self.req_date,
            "huifu_id":self.huifu_id,
            "device_id":self.device_id
        }
        required_params.update(extend_infos)
        return request_post(V2_TERMINALDEVICE_MANAGE_BIND, required_params)
