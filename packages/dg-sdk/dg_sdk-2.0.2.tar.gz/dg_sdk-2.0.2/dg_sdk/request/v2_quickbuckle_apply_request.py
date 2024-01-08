from dg_sdk.core.request_tools import request_post
from dg_sdk.request.request_api_urls import V2_QUICKBUCKLE_APPLY



class V2QuickbuckleApplyRequest(object):
    """
    快捷绑卡申请接口
    """

    # 请求日期
    req_date = ""
    # 请求流水号
    req_seq_id = ""
    # 汇付客户Id
    huifu_id = ""
    # 商户用户id
    out_cust_id = ""
    # 订单号
    order_id = ""
    # 订单日期
    order_date = ""
    # 银行卡号
    card_id = ""
    # 银行卡开户姓名
    card_name = ""
    # 银行卡绑定证件类型
    cert_type = ""
    # 银行卡绑定身份证
    cert_id = ""
    # 个人证件有效期类型
    cert_validity_type = ""
    # 个人证件有效期起始日
    cert_begin_date = ""
    # 个人证件有效期到期日长期有效不填；&lt;font color&#x3D;&quot;green&quot;&gt;示例值：20420905&lt;/font&gt;
    cert_end_date = ""
    # 银行卡绑定手机号
    card_mp = ""
    # CVV2信用卡交易专用需要密文传输。&lt;br/&gt;使用汇付RSA公钥加密(加密前3位，加密后最长2048位），[参见参考文档](https://paas.huifu.com/partners/guide/#/api_jiami_jiemi)；&lt;br/&gt;&lt;font color&#x3D;&quot;green&quot;&gt;示例值：Ly+fnExeyPOTzfOtgRRur77nJB9TAe4PGgK9M……fc6XJXZss&#x3D;&lt;/font&gt;
    vip_code = ""
    # 卡有效期信用卡交易专用，格式：MMYY，需要密文传输；&lt;br/&gt;使用汇付RSA公钥加密(加密前4位，加密后最长2048位），[参见参考文档](https://paas.huifu.com/partners/guide/#/api_jiami_jiemi)；&lt;br/&gt;&lt;font color&#x3D;&quot;green&quot;&gt;示例值：Ly+fnExeyPOTzfOtgRRur77nJB9TAe4PGgK9M……fc6XJXZss&#x3D;JXZss&#x3D;&lt;/font&gt;
    expiration = ""
    # 挂网协议编号授权信息(招行绑卡需要上送)；&lt;font color&#x3D;&quot;green&quot;&gt;示例值：34463343&lt;/font&gt;
    protocol_no = ""
    # 设备信息域 
    trx_device_inf = ""

    def post(self, extend_infos):
        """
        快捷绑卡申请接口

        :param extend_infos: 扩展字段字典
        :return:
        """

        required_params = {
            "req_date":self.req_date,
            "req_seq_id":self.req_seq_id,
            "huifu_id":self.huifu_id,
            "out_cust_id":self.out_cust_id,
            "order_id":self.order_id,
            "order_date":self.order_date,
            "card_id":self.card_id,
            "card_name":self.card_name,
            "cert_type":self.cert_type,
            "cert_id":self.cert_id,
            "cert_validity_type":self.cert_validity_type,
            "cert_begin_date":self.cert_begin_date,
            "cert_end_date":self.cert_end_date,
            "card_mp":self.card_mp,
            "vip_code":self.vip_code,
            "expiration":self.expiration,
            "protocol_no":self.protocol_no,
            "trx_device_inf":self.trx_device_inf
        }
        required_params.update(extend_infos)
        return request_post(V2_QUICKBUCKLE_APPLY, required_params)
