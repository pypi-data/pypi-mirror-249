import unittest
import dg_sdk
import json
from demo.demo_config import *


def getSignUserInfo():
    dto = dict()
    # 签约人类型
    # dto["type"] = "test"
    # 姓名
    # dto["name"] = ""
    # 手机号
    # dto["mobile_no"] = ""
    # 身份证
    # dto["cert_no"] = ""
    # 身份证照片-人像面
    # dto["identity_front_file_id"] = ""
    # 身份证照片-国徽面
    # dto["identity_back_file_id"] = ""
    # 法人授权书
    # dto["auth_file_id"] = ""

    return json.dumps(dto)

def getSettleConfig():
    dto = dict()
    # 结算开关
    dto["settle_status"] = "1"
    # 结算周期
    dto["settle_cycle"] = "T1"
    # 结算手续费外扣商户号结算手续费外扣商户号，填写承担手续费的汇付商户号；当out_settle_flag&#x3D;1时必填，否则非必填；&lt;font color&#x3D;&quot;green&quot;&gt;示例值：6666000123123123 &lt;/font&gt;
    dto["out_settle_huifuid"] = "6666000003078904"
    # 起结金额
    dto["min_amt"] = "3.00"
    # 留存金额
    dto["remained_amt"] = "22.00"
    # 结算摘要
    dto["settle_abstract"] = "我这里显示结算摘要"
    # 手续费外扣标记
    dto["out_settle_flag"] = "2"
    # 结算手续费外扣时的账户类型
    dto["out_settle_acct_type"] = ""
    # 节假日结算手续费率
    dto["fixed_ratio"] = "2.00"
    # 结算批次号
    # dto["settle_batch_no"] = ""
    # 结算方式
    # dto["settle_pattern"] = ""
    # 是否优先到账
    # dto["is_priority_receipt"] = ""
    # 自定义结算处理时间
    # dto["settle_time"] = ""

    return json.dumps(dto)

def getCashConfig():
    dto = dict()
    # 状态
    dto["switch_state"] = "1"
    # 取现手续费率（%）fix_amt与fee_rat至少填写一项，单位%，需保留小数点后两位，取值范围[0.00,100.00]，不收费请填写0.00；&lt;font color&#x3D;&quot;green&quot;&gt;示例值：0.05&lt;/font&gt;&lt;br/&gt;注：如果fix_amt与fee_rate都填写了则手续费&#x3D;fix_amt+支付金额\*fee_rate
    dto["fee_rate"] = "5.50"
    # 业务类型
    dto["cash_type"] = "D0"
    # 提现手续费（固定/元）
    dto["fix_amt"] = "4.00"
    # 是否交易手续费外扣
    # dto["out_fee_flag"] = ""
    # 手续费承担方
    # dto["out_fee_huifu_id"] = ""
    # 手续费外扣的账户类型
    # dto["out_fee_acct_type"] = ""

    dtoList = [dto]
    return json.dumps(dtoList)

def getCardInfo():
    dto = dict()
    # 结算账户类型
    dto["card_type"] = "0"
    # 结算账户名
    dto["card_name"] = "上海尼博网络科技有限公司"
    # 结算账号
    dto["card_no"] = "1001265009300682579"
    # 银行所在省参考[地区编码](https://paas.huifu.com/partners/api/#/csfl/api_csfl_dqbm)；&lt;font color&#x3D;&quot;green&quot;&gt;示例值：310000 &lt;/font&gt;；如修改省市要级联修改&lt;br/&gt;当card_type&#x3D;0时非必填， 当card_type&#x3D;1或2时必填
    dto["prov_id"] = "310000"
    # 银行所在市参考[地区编码](https://paas.huifu.com/partners/api/#/csfl/api_csfl_dqbm)；&lt;font color&#x3D;&quot;green&quot;&gt;示例值：310100 &lt;/font&gt;；如修改省市要级联修改&lt;br/&gt;当card_type&#x3D;0时非必填， 当card_type&#x3D;1或2时必填
    dto["area_id"] = "310100"
    # 支行联行号参考：[银行支行编码](https://paas.huifu.com/partners/api/#/csfl/api_csfl_yhzhbm) 当card_type&#x3D;0时必填， 当card_type&#x3D;1或2时非必填 &lt;font color&#x3D;&quot;green&quot;&gt;示例值：102290026507&lt;/font&gt;
    dto["branch_code"] = "102290026507"
    # 持卡人证件类型持卡人证件类型，参见《[自然人证件类型](https://paas.huifu.com/partners/api/#/api_ggcsbm?id&#x3D;%e8%87%aa%e7%84%b6%e4%ba%ba%e8%af%81%e4%bb%b6%e7%b1%bb%e5%9e%8b)》。&lt;br/&gt; 当card_type&#x3D;0时为空， 当card_type&#x3D;1或2时必填； &lt;font color&#x3D;&quot;green&quot;&gt;示例值：00&lt;/font&gt;
    dto["cert_type"] = "00"
    # 持卡人证件有效期类型0：非长期有效, 1：长期有效, &lt;font color&#x3D;&quot;green&quot;&gt;示例值：0&lt;/font&gt;&lt;br/&gt;当card_type&#x3D;0时为空； 当card_type&#x3D;1或2时必填；
    dto["cert_validity_type"] = "0"
    # 持卡人证件有效期开始日期日期格式：yyyyMMdd，以北京时间为准； 当card_type&#x3D;0时为空， 当card_type&#x3D;1或2时必填， &lt;font color&#x3D;&quot;green&quot;&gt;示例值：20220125 &lt;/font&gt;
    dto["cert_begin_date"] = "20180106"
    # 持卡人证件有效期截止日期日期格式：yyyyMMdd，以北京时间为准。&lt;font color&#x3D;&quot;green&quot;&gt;示例值：20220125&lt;/font&gt;&lt;br/&gt;  当cert_validity_type&#x3D;0时必填；当cert_validity_type&#x3D;1时为空
    dto["cert_end_date"] = "20380106"
    # 开户许可证开户许可证图片文件，请填写图片file_id，可通过 [商户图片上传](https://paas.huifu.com/partners/api/#/shgl/shjj/api_shjj_shtpsc) 接口获取，文件类型F08；&lt;br/&gt;企业商户需要，结算账号为对公账户，且开通全域资金管理必填；&lt;br/&gt;&lt;font color&#x3D;&quot;green&quot;&gt;示例值：57cc7f00-600a-33ab-b614-6221bbf2e529&lt;/font&gt;
    dto["reg_acct_pic"] = "d1451277-85c6-3177-ac3d-a8be47b9ae9d"
    # 法人身份证正面法人身份证正面图片文件，请填写图片file_id，可通过 [商户图片上传](https://paas.huifu.com/partners/api/#/shgl/shjj/api_shjj_shtpsc) 接口获取，文件类型F02；&lt;font color&#x3D;&quot;green&quot;&gt;示例值：57cc7f00-600a-33ab-b614-6221bbf2e529 &lt;/font&gt;
    dto["legal_cert_front_pic"] = "d1451277-85c6-3177-ac3d-a8be47b9ae9d"
    # 法人身份证反面法人身份证反面图片文件，请填写图片file_id，可通过 [商户图片上传](https://paas.huifu.com/partners/api/#/shgl/shjj/api_shjj_shtpsc) 接口获取，文件类型F03；&lt;font color&#x3D;&quot;green&quot;&gt;示例值：57cc7f00-600a-33ab-b614-6221bbf2e529&lt;/font&gt;
    dto["legal_cert_back_pic"] = "d1451277-85c6-3177-ac3d-a8be47b9ae9d"
    # 公司照片一公司照片一图片文件，请填写图片file_id，可通过 [商户图片上传](https://paas.huifu.com/partners/api/#/shgl/shjj/api_shjj_shtpsc) 接口获取，文件类型F22（店铺门头照）；&lt;br/&gt;&lt;font color&#x3D;&quot;green&quot;&gt;示例值：57cc7f00-600a-33ab-b614-6221bbf2e529&lt;/font&gt;
    dto["comp_pic1"] = "d1451277-85c6-3177-ac3d-a8be47b9ae9d"
    # 公司照片二公司照片二图片文件，请填写图片file_id，可通过 [商户图片上传](https://paas.huifu.com/partners/api/#/shgl/shjj/api_shjj_shtpsc) 接口获取，文件类型F24（店铺内景照）；&lt;br/&gt;&lt;font color&#x3D;&quot;green&quot;&gt;示例值：57cc7f00-600a-33ab-b614-6221bbf2e529&lt;/font&gt;
    dto["comp_pic2"] = "d1451277-85c6-3177-ac3d-a8be47b9ae9d"
    # 公司照片三公司照片三图片文件，请填写图片file_id，可通过 [商户图片上传](https://paas.huifu.com/partners/api/#/shgl/shjj/api_shjj_shtpsc) 接口获取，文件类型F105（店铺收银台或前台）；&lt;br/&gt;&lt;font color&#x3D;&quot;green&quot;&gt;示例值：57cc7f00-600a-33ab-b614-6221bbf2e529&lt;/font&gt;
    dto["comp_pic3"] = "d1451277-85c6-3177-ac3d-a8be47b9ae9d"
    # 结算卡正面结算卡正面图片文件对私结算必填，请填写图片file_id，可通过 [商户图片上传](https://paas.huifu.com/partners/api/#/shgl/shjj/api_shjj_shtpsc) 接口获取，文件类型F13；&lt;br/&gt;&lt;font color&#x3D;&quot;green&quot;&gt;示例值：57cc7f00-600a-33ab-b614-6221bbf2e529&lt;/font&gt;
    dto["settle_card_front_pic"] = "1277-85c6-3177-ac3d-a8be47b9ae9d"
    # 结算卡反面结算卡反面图片文件对私结算必填，请填写图片file_id，可通过 [商户图片上传](https://paas.huifu.com/partners/api/#/shgl/shjj/api_shjj_shtpsc) 接口获取，文件类型F14；&lt;br/&gt;&lt;font color&#x3D;&quot;green&quot;&gt;示例值：57cc7f00-600a-33ab-b614-6221bbf2e529&lt;/font&gt;
    dto["settle_card_back_pic"] = "d1451277-85c6-3177-ac3d-a8be47b9ae9d"
    # 结算人身份证正面结算人身份证正面图片文件对私结算必填，请填写图片file_id，可通过 [商户图片上传](https://paas.huifu.com/partners/api/#/shgl/shjj/api_shjj_shtpsc) 接口获取，文件类型F55；&lt;br/&gt;&lt;font color&#x3D;&quot;green&quot;&gt;示例值：57cc7f00-600a-33ab-b614-6221bbf2e529&lt;/font&gt;
    dto["settle_cert_front_pic"] = "d1451277-85c6-3177-ac3d-a8be47b9ae9d"
    # 结算人身份证反面结算人身份证反面图片文件对私结算必填，请填写图片file_id，可通过 [商户图片上传](https://paas.huifu.com/partners/api/#/shgl/shjj/api_shjj_shtpsc) 接口获取，文件类型F56；&lt;br/&gt;&lt;font color&#x3D;&quot;green&quot;&gt;示例值：57cc7f00-600a-33ab-b614-6221bbf2e529  &lt;/font&gt;
    dto["settle_cert_back_pic"] = "d1451277-85c6-3177-ac3d-a8be47b9ae9d"
    # 银行编码
    dto["bank_code"] = "01020000"
    # 开户支行名称
    dto["branch_name"] = "中国工商银行股份有限公司上海市中山北路支行"
    # 持卡人证件号码
    dto["cert_no"] = "320923199111206319"
    # 结算人手机号
    dto["mp"] = "18221987178"

    return json.dumps(dto)


def build_extend_infos():
    """
    非必填字段

    :return: 非必填字段组成的字典
    """
    extend_infos = dict()
    # 商户简称
    extend_infos["short_name"] = "尼博网络"
    # 营业执照类型
    # extend_infos["license_type"] = ""
    # 营业执照有效期类型
    extend_infos["license_validity_type"] = "0"
    # 营业执照有效期开始日期
    extend_infos["license_begin_date"] = "20200814"
    # 营业执照有效期截止日期
    extend_infos["license_end_date"] = "20400813"
    # 注册省
    extend_infos["reg_prov_id"] = "310000"
    # 注册市
    extend_infos["reg_area_id"] = "310100"
    # 注册区
    extend_infos["reg_district_id"] = "310120"
    # 注册详细地址
    extend_infos["reg_detail"] = "台州市宜山路700解放2路715"
    # 法人姓名
    extend_infos["legal_name"] = "沈荣"
    # 法人证件类型
    extend_infos["legal_cert_type"] = "00"
    # 法人证件号码
    extend_infos["legal_cert_no"] = "320923199111206319"
    # 法人证件有效期类型
    extend_infos["legal_cert_validity_type"] = "0"
    # 法人证件有效期开始日期
    extend_infos["legal_cert_begin_date"] = "20200814"
    # 法人证件有效期截止日期
    extend_infos["legal_cert_end_date"] = "20400813"
    # 经营省
    extend_infos["prov_id"] = "310000"
    # 经营市
    extend_infos["area_id"] = "310100"
    # 经营区
    extend_infos["district_id"] = "310105"
    # 经营详细地址
    extend_infos["detail_addr"] = "徐州市徐汇区宜山路7497号"
    # 联系人姓名
    extend_infos["contact_name"] = "我是联系人"
    # 联系人手机号
    extend_infos["contact_mobile_no"] = "15556622331"
    # 联系人电子邮箱
    extend_infos["contact_email"] = "mei.zhang@huifu.com"
    # 客服电话
    extend_infos["service_phone"] = "15556622368"
    # 小票名称
    extend_infos["receipt_name"] = "小票上的名称"
    # 所属行业（MCC）
    extend_infos["mcc"] = "5411"
    # 结算卡信息配置
    extend_infos["card_info"] = getCardInfo()
    # 取现信息配置
    extend_infos["cash_config"] = getCashConfig()
    # 结算规则配置
    extend_infos["settle_config"] = getSettleConfig()
    # 异步通知地址
    extend_infos["async_return_url"] = "archer://C_SSPM_NSPOSM_BUSIRESULT"
    # D1结算协议图片文件
    # extend_infos["settle_agree_pic"] = ""
    # 商户英文名称
    # extend_infos["mer_en_name"] = ""
    # 商户主页URL
    # extend_infos["mer_url"] = ""
    # 商户ICP备案编号
    # extend_infos["mer_icp"] = ""
    # 基本存款账户编号或核准号
    # extend_infos["open_licence_no"] = ""
    # 签约人
    # extend_infos["sign_user_info"] = getSignUserInfo()
    # 营业执照图片
    # extend_infos["license_pic"] = ""
    # 授权委托书
    # extend_infos["auth_enturst_pic"] = ""
    # 组织机构代码证
    # extend_infos["org_code_pic"] = ""
    # 税务登记证
    # extend_infos["tax_reg_pic"] = ""
    return extend_infos


class TestV2MerchantBasicdataModifyRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 商户基本信息修改(2022) - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2MerchantBasicdataModifyRequest()
        request.req_seq_id = ""
        request.req_date = ""
        request.upper_huifu_id = "6666000021000000"
        request.huifu_id = "6666000107932702"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""