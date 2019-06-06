# -*- coding: utf-8 -*-
#from wmj
from piaoxiaomi_api import save_to_csv
from piaoxiaomi_api import get_invoice_data
from bot_wechat_invoice import invoice_bot
from bot_wechat_invoice import send_group_message
from baidu_ai import get_commodity_data
from question_dict import question_dict
from wxpy import *
import time


correct_info = {
    '购方名称': '甘肃省水利水电勘测设计研究院',
    '购方纳税人识别号': '620102438002318'

}

bot = Bot()  # 实例化机器人对象
group_name = '6666'

# # 在win系统第一次运行时，在该系统没有保存该群聊信息，需要首先发送一条信息
# print('请在目标群聊中输入一句话唤醒微信机器人')
# content = input()

send_group_message(bot, group_name, '6666～～')
invoice_data_list = []  # 存储识别后的发票信息的列表


def check_info(field, bot, group_name):
    """
    根据传入的字段进行信息校验，并发送信息
    :param field:
    :return:
    """
    send_group_message(bot, group_name, '识别的{}为：'.format(field) + invoice_data[field])
    if invoice_data[field] == correct_info[field]:
        send_group_message(bot, group_name, '{}正确'.format(field))
    else:
        send_group_message(bot, group_name, '{}错误！！'.format(field))
        send_group_message(bot, group_name, '正确的{}为：'.format(field) + correct_info[field])


while True:
    # 1 延迟：扫描微信群聊信息的时间间隔
    time.sleep(1)
    # 2 获取目标群聊中的目标信息列表：
    # 第一个列表为发票的绝对路径列表
    # 第二个列表为问题关键字列表
    info_list = invoice_bot(bot, group_name)
    # 3 判断目标信息列表，如果获取到了目标信息，则执行；未获取到则不执行，进入下一次循环
    if info_list:
        # 3.1 发送发票识别信息
        pic_list = info_list[0]  # 发票图片绝对地址列表
        for pic in pic_list:
            # 3.1.1 发送发票校验结果-票小秘api
            invoice_data = get_invoice_data(pic)
            if invoice_data:  # 如果能够识别发票信息，那么查看信息
                check_info('购方名称', bot, group_name)
                check_info('购方纳税人识别号', bot, group_name)
                invoice_data_list.append(invoice_data.values())  # 将识别后的发票数据添加到列表
                today = time.strftime("%y%m%d", time.localtime())  # 获取今日日期
                save_to_csv(invoice_data_list, today)  # 将发票列表信息存入本地csv，文件名为今日的日期
                invoice_data_list = []  # 清空原列表
            # 3.1.2 发送货物信息-百度api
            commodity_datas = get_commodity_data(pic)  # 获取识别后的货物信息
            if commodity_datas:  # 如果能够识别，那么就读取识别后的信息
                for commodity in commodity_datas:
                    commodity_info = '货物名称：{}\n规格型号：{}\n单位：{}\n数量：{}\n单价：{}\n金额：{}\n税率：{}\n税额{}\n'\
                        .format(commodity['货物名称'], commodity['规格型号'], commodity['单位'], commodity['数量'],
                                commodity['单价'], commodity['金额'], commodity['税率'], commodity['税额'])
                    send_group_message(bot, group_name, commodity_info)  # 发送识别后的数据到群聊
        # 3.2 发送问询信息
        question_keys_list = info_list[1]  # 问题关键字列表
        for key in question_keys_list:
            send_group_message(bot, group_name, '{}：{}'.format(key, question_dict[key]))  # 发送字典中的预置信息
