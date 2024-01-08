from dg_sdk.core.request_tools import request_post
from dg_sdk.request.request_api_urls import V2_MERCHANT_BASICDATA_INDV



class V2MerchantBasicdataIndvRequest(object):
    """
    个人商户基本信息入驻(2022)
    """

    # 请求流水号
    req_seq_id = ""
    # 请求日期
    req_date = ""
    # 上级主体ID
    upper_huifu_id = ""
    # 商户名
    reg_name = ""
    # 经营省
    prov_id = ""
    # 经营市
    area_id = ""
    # 经营区
    district_id = ""
    # 经营详细地址
    detail_addr = ""
    # 联系人姓名
    contact_name = ""
    # 联系人手机号
    contact_mobile_no = ""
    # 联系人电子邮箱
    contact_email = ""
    # 结算卡信息配置
    card_info = ""

    def post(self, extend_infos):
        """
        个人商户基本信息入驻(2022)

        :param extend_infos: 扩展字段字典
        :return:
        """

        required_params = {
            "req_seq_id":self.req_seq_id,
            "req_date":self.req_date,
            "upper_huifu_id":self.upper_huifu_id,
            "reg_name":self.reg_name,
            "prov_id":self.prov_id,
            "area_id":self.area_id,
            "district_id":self.district_id,
            "detail_addr":self.detail_addr,
            "contact_name":self.contact_name,
            "contact_mobile_no":self.contact_mobile_no,
            "contact_email":self.contact_email,
            "card_info":self.card_info
        }
        required_params.update(extend_infos)
        return request_post(V2_MERCHANT_BASICDATA_INDV, required_params)
