from dg_sdk.core.request_tools import request_post
from dg_sdk.request.request_api_urls import V2_MERCHANT_ACTIVITY_ADD



class V2MerchantActivityAddRequest(object):
    """
    商户活动报名
    """

    # 请求日期
    req_date = ""
    # 请求流水号
    req_seq_id = ""
    # 汇付客户Id
    huifu_id = ""
    # 营业执照图片
    bl_photo = ""
    # 店内环境图片
    dh_photo = ""
    # 手续费类型
    fee_type = ""
    # 整体门面图片（门头照）
    mm_photo = ""
    # 收银台照片
    syt_photo = ""
    # 支付通道
    pay_way = ""

    def post(self, extend_infos):
        """
        商户活动报名

        :param extend_infos: 扩展字段字典
        :return:
        """

        required_params = {
            "req_date":self.req_date,
            "req_seq_id":self.req_seq_id,
            "huifu_id":self.huifu_id,
            "bl_photo":self.bl_photo,
            "dh_photo":self.dh_photo,
            "fee_type":self.fee_type,
            "mm_photo":self.mm_photo,
            "syt_photo":self.syt_photo,
            "pay_way":self.pay_way
        }
        required_params.update(extend_infos)
        return request_post(V2_MERCHANT_ACTIVITY_ADD, required_params)
