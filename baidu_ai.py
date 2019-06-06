# -*- coding: utf-8 -*-
from aip import AipOcr


def get_file_content(file_path):
    """
    以二进制格式打开图片
    :param file_path: 图片的存放位置
    :return: 二进制格式的图片数据
    """
    with open(file_path, 'rb') as fp:  # 以二进制格式打开图片
        return fp.read()


def baidu_api(pic_data):
    """
    调用百度API识别发票，返回识别后的字段
    :param pic_data: 图片数据
    :return:
    """
    # 百度ai客户端设置
    APP_ID = 'XXXX'
    API_KEY = 'XXXX'
    SECRET_KEY = 'XXXX'
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    invoice_data_raw = client.vatInvoice(pic_data)  # 调用百度api识别发票数据
    CommodityNames = invoice_data_raw['words_result']['CommodityName']  # 货物名称列表
    CommodityTypes = invoice_data_raw['words_result']['CommodityType']  # 规格型号列表
    CommodityUnits = invoice_data_raw['words_result']['CommodityUnit']  # 单位列表
    CommodityNums = invoice_data_raw['words_result']['CommodityNum']  # 数量列表
    CommodityPrices = invoice_data_raw['words_result']['CommodityPrice']  # 单价列表
    CommodityAmounts = invoice_data_raw['words_result']['CommodityAmount']  # 金额列表
    CommodityTaxRates = invoice_data_raw['words_result']['CommodityTaxRate']  # 税率列表
    CommodityTaxs = invoice_data_raw['words_result']['CommodityTax']  # 税额列表
    # print(CommodityNames)
    Commoditydatas = []
    for CommodityName, CommodityType, CommodityUnit, CommodityNum, CommodityPrice, CommodityAmount, CommodityTaxRate, CommodityTax in zip(
            CommodityNames, CommodityTypes, CommodityUnits, CommodityNums, CommodityPrices, CommodityAmounts,
            CommodityTaxRates, CommodityTaxs):
        Commoditydata = {
            '货物名称': CommodityName['word'],
            '规格型号': CommodityType['word'],
            '单位': CommodityUnit['word'],
            '数量': CommodityNum['word'],
            '单价': CommodityPrice['word'],
            '金额': CommodityAmount['word'],
            '税率': CommodityTaxRate['word'],
            '税额': CommodityTax['word']
        }
        Commoditydatas.append(Commoditydata)
    return Commoditydatas


def get_commodity_data(pic_path):
    """
    传入图片绝对路径，返回识别后的货物信息，如果无法识别则返回None
    :param pic_path:
    :return:
    """
    image = get_file_content(pic_path)
    try:
        data_baidu = baidu_api(image)
    except:
        return None
    return data_baidu


# data = get_commodity_data('/Users/mengfanjie/Desktop/IMG_7642.JPG')
# print('666')
# print('666')
# a = 6
