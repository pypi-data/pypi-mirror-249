import unittest
import dg_sdk
import json
from demo.demo_config import *


def getFileList():
    dto = dict()
    # 文件类型
    dto["file_type"] = "F02"
    # 文件jfileID
    dto["file_id"] = "99e00421-dad7-3334-9538-4f2ad10612d5"
    # 文件名称
    dto["file_name"] = "企业营业执照1.jpg"

    dtoList = [dto]
    return json.dumps(dtoList)

def getCashConfig():
    dto = dict()
    # 开通状态
    dto["switch_state"] = "1"
    # 取现手续费率（%）fix_amt与fee_rate至少填写一项，单位%，需保留小数点后两位，取值范围[0.00,100.00]，不收费请填写0.00；&lt;font color&#x3D;&quot;green&quot;&gt;示例值：0.05&lt;/font&gt;&lt;br/&gt;注：如果fix_amt与fee_rate都填写了则手续费&#x3D;fix_amt+支付金额\*fee_rate
    dto["fee_rate"] = "0.05"
    # 业务类型
    dto["cash_type"] = "D0"
    # 提现手续费（固定/元）
    dto["fix_amt"] = "3"
    # 是否交易手续费外扣
    dto["out_fee_flag"] = "1"
    # 手续费承担方
    dto["out_fee_huifu_id"] = "6666000104633228"
    # 交易手续费外扣的账户类型
    dto["out_fee_acct_type"] = "05"
    # 是否优先到账
    # dto["is_priority_receipt"] = ""

    dtoList = [dto]
    return json.dumps(dtoList)

def getCardInfo():
    dto = dict()
    # 卡类型
    dto["card_type"] = "0"
    # 卡户名
    dto["card_name"] = "陈立一"
    # 卡号
    dto["card_no"] = "6217001210064762000"
    # 银行所在省
    dto["prov_id"] = "310000"
    # 银行所在市
    dto["area_id"] = "310100"
    # 银行号对公时必填，对私可以为空；[参见银行编码](https://paas.huifu.com/partners/api/#/csfl/api_csfl_yhbm)；&lt;font color&#x3D;&quot;green&quot;&gt;示例值：01020000&lt;/font&gt;
    dto["bank_code"] = "01050000"
    # 支行联行号对公时联行号、支行名称二选一必填，[点击查看](https://paas.huifu.com/partners/api/#/csfl/api_csfl_yhzhbm)；&lt;font color&#x3D;&quot;green&quot;&gt;示例值：102290026507&lt;/font&gt;
    dto["branch_code"] = "105305264815"
    # 支行名称对公时联行号、支行名称二选一必填，&lt;br/&gt;&lt;font color&#x3D;&quot;green&quot;&gt;示例值：中国工商银行上海市中山北路支行&lt;/font&gt;
    dto["branch_name"] = "中国建设银行股份有限公司上海平凉路支行"
    # 持卡人证件类型
    dto["cert_type"] = "00"
    # 持卡人证件号码
    dto["cert_no"] = "110101197003077000"
    # 持卡人证件有效期类型
    dto["cert_validity_type"] = "0"
    # 持卡人证件有效期起始日期
    dto["cert_begin_date"] = "20210806"
    # 持卡人证件有效期截止日期
    dto["cert_end_date"] = "20410806"
    # 银行卡绑定手机号
    dto["mp"] = "15556622000"

    return json.dumps(dto)

def getSettleConfig():
    dto = dict()
    # 开通状态
    dto["settle_status"] = "1"
    # 结算周期
    dto["settle_cycle"] = "D1"
    # 结算批次号settle_pattern为P0时选填；&lt;br/&gt;0点昨日余额结算批次:0,&lt;/br&gt;1点余额结算批次:100,&lt;/br&gt;2点余额结算批次:200,&lt;/br&gt;3点余额结算批次:300,&lt;/br&gt;4点余额结算批次:400,&lt;/br&gt;5点余额结算批次:500,&lt;/br&gt;6点余额结算批次:600,&lt;/br&gt;7点余额结算批次:700,&lt;/br&gt;8点余额结算批次:800,&lt;/br&gt;9点余额结算批次:900,&lt;/br&gt;10点余额结算批次:1000,&lt;/br&gt;11点余额结算批次:1100,&lt;/br&gt;12点余额结算批次:1200&lt;/br&gt;&lt;font color&#x3D;&quot;green&quot;&gt;示例值：1000&lt;/font&gt;
    dto["settle_batch_no"] = "0"
    # 是否优先到账settle_pattern为P0时选填， Y：是 N：否（为空默认取值）；&lt;font color&#x3D;&quot;green&quot;&gt;示例值：Y&lt;/font&gt;
    dto["is_priority_receipt"] = "Y"
    # 自定义结算处理时间settle_pattern为P1时必填， 格式：HHmmss；&lt;font color&#x3D;&quot;green&quot;&gt;示例值：103000&lt;/font&gt;
    dto["settle_time"] = ""
    # 节假日结算手续费率(%)
    dto["fixed_ratio"] = "0.1"
    # 起结金额
    dto["min_amt"] = "0.1"
    # 结算手续费外扣时的账户类型
    dto["out_settle_acct_type"] = "05"
    # 手续费外扣标记
    dto["out_settle_flag"] = "1"
    # 结算手续费外扣时的汇付ID
    dto["out_settle_huifuid"] = "6666000104633228"
    # 留存金额
    dto["remained_amt"] = "0.1"
    # 结算摘要
    dto["settle_abstract"] = "吃吃"
    # 结算方式
    dto["settle_pattern"] = "P0"

    return json.dumps(dto)


def build_extend_infos():
    """
    非必填字段

    :return: 非必填字段组成的字典
    """
    extend_infos = dict()
    # 结算信息配置
    extend_infos["settle_config"] = getSettleConfig()
    # 结算卡信息
    extend_infos["card_info"] = getCardInfo()
    # 取现配置列表
    extend_infos["cash_config"] = getCashConfig()
    # 文件列表
    extend_infos["file_list"] = getFileList()
    # 延迟入账开关
    # extend_infos["delay_flag"] = ""
    # 异步请求地址
    extend_infos["async_return_url"] = "//http://service.example.com/to/path"
    return extend_infos


class TestV2UserBusiModifyRequestDemo(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(PRIVATE_KEY, PUBLIC_KEY, SYS_ID, PRODUCT_ID)

        print("setup")


    # 用户业务入驻修改 - 示例
    def test_request(self):

        # 接口请求对象
        request = dg_sdk.V2UserBusiModifyRequest()
        request.req_seq_id = ""
        request.req_date = ""
        request.upper_huifu_id = "6666000104633228"
        request.huifu_id = "6666000104896342"

        # 所有非必填字段字典
        extend_infos = build_extend_infos()

        result = request.post(extend_infos)

        print(result)
        assert result["resp_code"] != ""