from dg_sdk.core.request_tools import request_post
from dg_sdk.request.request_api_urls import V2_MERCHANT_BASICDATA_ENT



class V2MerchantBasicdataEntRequest(object):
    """
    企业商户基本信息入驻(2022)
    """

    # 请求流水号
    req_seq_id = ""
    # 请求日期
    req_date = ""
    # 上级主体ID
    upper_huifu_id = ""
    # 商户名称
    reg_name = ""
    # 商户简称
    short_name = ""
    # 公司类型
    ent_type = ""
    # 营业执照编号
    license_code = ""
    # 营业执照有效期类型
    license_validity_type = ""
    # 营业执照有效期开始日期
    license_begin_date = ""
    # 营业执照有效期截止日期日期格式：yyyyMMdd，以北京时间为准。&lt;font color&#x3D;&quot;green&quot;&gt;示例值：20220125&lt;/font&gt;&lt;br/&gt;  当license_validity_type&#x3D;0时必填  ;当license_validity_type&#x3D;1时为空；当使用总部资质时不填
    license_end_date = ""
    # 注册省
    reg_prov_id = ""
    # 注册市
    reg_area_id = ""
    # 注册区
    reg_district_id = ""
    # 注册详细地址
    reg_detail = ""
    # 法人姓名
    legal_name = ""
    # 法人证件类型
    legal_cert_type = ""
    # 法人证件号码
    legal_cert_no = ""
    # 法人证件有效期类型
    legal_cert_validity_type = ""
    # 法人证件有效期开始日期
    legal_cert_begin_date = ""
    # 法人证件有效期截止日期日期格式：yyyyMMdd，以北京时间为准。  &lt;font color&#x3D;&quot;green&quot;&gt;示例值：20220125&lt;/font&gt;&lt;br/&gt;当legal_cert_validity_type&#x3D;0时必填 ；当legal_cert_validity_type&#x3D;1时为空 ；当使用总部资质时不填
    legal_cert_end_date = ""
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
    # 客服电话
    service_phone = ""
    # 经营类型
    busi_type = ""
    # 小票名称
    receipt_name = ""
    # 所属行业
    mcc = ""
    # 结算卡信息配置
    card_info = ""
    # 基本存款账户编号或核准号基本存款账户信息请填写基本存款账户编号；开户许可证请填写核准号 ；&lt;br/&gt;当注册地址或经营地址为如下地区时必填：浙江,海南,重庆,河南,江苏,宁波市,黑龙江,吉林,湖南,贵州,陕西,湖北 &lt;br/&gt;当使用总部资质时不填 ；&lt;font color&#x3D;&quot;green&quot;&gt;示例值：J2900123456789&lt;/font&gt;
    open_licence_no = ""
    # 总部汇付Id如果headOfficeFlag&#x3D;0，useHeadInfoFlag&#x3D;Y,且head_huifu_id不为空则基本信息部分复用总部的基本信息。&lt;br/&gt;如果head_office_flag&#x3D;0，则字段必填,如果head_office_flag&#x3D;1，总部汇付Id不可传&lt;br/&gt;&lt;font color&#x3D;&quot;green&quot;&gt;示例值：6666000123123123&lt;/font&gt;
    head_huifu_id = ""

    def post(self, extend_infos):
        """
        企业商户基本信息入驻(2022)

        :param extend_infos: 扩展字段字典
        :return:
        """

        required_params = {
            "req_seq_id":self.req_seq_id,
            "req_date":self.req_date,
            "upper_huifu_id":self.upper_huifu_id,
            "reg_name":self.reg_name,
            "short_name":self.short_name,
            "ent_type":self.ent_type,
            "license_code":self.license_code,
            "license_validity_type":self.license_validity_type,
            "license_begin_date":self.license_begin_date,
            "license_end_date":self.license_end_date,
            "reg_prov_id":self.reg_prov_id,
            "reg_area_id":self.reg_area_id,
            "reg_district_id":self.reg_district_id,
            "reg_detail":self.reg_detail,
            "legal_name":self.legal_name,
            "legal_cert_type":self.legal_cert_type,
            "legal_cert_no":self.legal_cert_no,
            "legal_cert_validity_type":self.legal_cert_validity_type,
            "legal_cert_begin_date":self.legal_cert_begin_date,
            "legal_cert_end_date":self.legal_cert_end_date,
            "prov_id":self.prov_id,
            "area_id":self.area_id,
            "district_id":self.district_id,
            "detail_addr":self.detail_addr,
            "contact_name":self.contact_name,
            "contact_mobile_no":self.contact_mobile_no,
            "contact_email":self.contact_email,
            "service_phone":self.service_phone,
            "busi_type":self.busi_type,
            "receipt_name":self.receipt_name,
            "mcc":self.mcc,
            "card_info":self.card_info,
            "open_licence_no":self.open_licence_no,
            "head_huifu_id":self.head_huifu_id
        }
        required_params.update(extend_infos)
        return request_post(V2_MERCHANT_BASICDATA_ENT, required_params)
