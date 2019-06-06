# -*- coding: utf-8 -*-

"""
模块功能：传入发票图片，返回识别后的发票数据
"""
import requests
import time
import hashlib
import traceback
import base64
import os
import csv


def get_file_content(file_path):
    """
    以二进制格式打开图片
    :param file_path: 图片的存放位置
    :return: 二进制格式的图片数据
    """
    with open(file_path, 'rb') as fp:  # 以二进制格式打开图片
        return fp.read()


def piaoxiaomi_api(pic_data):
    """
    调用票小秘接口，返回识别后的发票数据
    :param pic_data:
    :return:
    """
    appkey = "XXXX"  # 这里输入提供的app_key
    appsecret = "XXXX"  # 这里输入提供的app_secret
    api_url = "XXXX"
    image_data = base64.b64encode(pic_data)  # base64编码
    try:
        # generate timestamp
        timestamp = int(time.time())
        # generate token
        m = hashlib.md5()
        token = appkey + "+" + str(timestamp) + "+" + appsecret
        m.update(token.encode('utf-8'))
        token = m.hexdigest()
        # post request
        data = {'image_data': image_data, 'app_key': appkey, 'timestamp': str(timestamp), 'token': token}
        r = requests.post(api_url, data=data)
        if r.status_code != 200:
            print("failed to get info from :")
        else:
            result = r.json()
            invoice_type = result['response']['data']['identify_results'][0]['type']
            if invoice_type == '10100' or invoice_type == '10101':  # 如果是增值税专票或普票，那么返回发票信息
                invoice_data_raw = result['response']['data']['identify_results'][0]['details']
                invoice_data_dict = {
                    '发票代码': invoice_data_raw['code'],
                    '发票号码': invoice_data_raw['number'],
                    '开票日期': invoice_data_raw['date'],
                    '合计金额': invoice_data_raw['pretax_amount'],
                    '价税合计': invoice_data_raw['total'],
                    '销售方名称': invoice_data_raw['seller'],
                    '销售方纳税人识别号': invoice_data_raw['seller_tax_id'],
                    '购方名称': invoice_data_raw['buyer'],
                    '购方纳税人识别号': invoice_data_raw['buyer_tax_id']
                }
            else:
                return None  # 如果不是增值税发票，那么返回None
    except:
        traceback.print_exc()
    return invoice_data_dict


def save_to_csv(invoice_data, file_name):
    path = os.getcwd()
    file = open(path + '/' + file_name + '.csv', 'a')
    writer = csv.writer(file)
    writer.writerows(invoice_data)
    file.close()


def get_invoice_data(file_path):
    """
    传入发票图片路径，返回识别后的发票数据
    :param file_path:发票图片路径
    :return: 识别后的发票数据
    """
    image = get_file_content(file_path)
    data_piaoxiaomi = piaoxiaomi_api(image)
    return data_piaoxiaomi


# # 注意使用绝对路径
# pic_path = '/Users/mengfanjie/Desktop/image/IMG_6957.JPG'
# # pic_path = '/Users/mengfanjie/Desktop/1.png'  # 非发票图片
# invoice_data = get_invoice_data(pic_path)
# # 从返回的数据中提取想要的数据并添加到二维列表
# print(invoice_data.values())





