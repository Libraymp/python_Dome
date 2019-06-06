# -*- coding: utf-8 -*-

import os
from question_dict import question_dict


def get_group_message(bot, group_name):
    """
    获取微信聊天中目标群的消息，同时移除聊天信息中的信息
    :param group_name:目标群聊名称
    :return group_invoice_messages:目标群聊信息
    """
    target_group_messages = []  # 存放目标群聊信息
    remove_messages = []
    # 1 获取目标群聊信息
    for message in bot.messages:
        if group_name == message.sender.name:  # 通过群聊名称来筛选属于该群的信息
            target_group_messages.append(message)
        remove_messages.append(message)  # 将要移除的信息添加到移除列表中
    # 2 清空所有群聊信息
    for remove_message in remove_messages:
        bot.messages.remove(remove_message)  # 移除已检查过的信息
    # 3 返回目标群聊信息
    return target_group_messages


def save_pic_file(message):
    """
    保存消息中的图片到当前文件夹，并返回保存文件的绝对路径
    :param message: 消息
    :return: 返回文件绝对路径
    """
    path = os.getcwd()  # 获取当前文件路径
    try:
        file_name = message.file_name.split('.')[0]  # 获取文件名称
        file_postfix = message.file_name.split('.')[-1]  # 获取文件后缀名
    except Exception as err:
        print(err)
        file_name = message.file_name
        file_postfix = ''
    file_whole_name = path + '/' + 'pic-' + file_name + '.' + file_postfix  # 文件全名
    message.get_file(file_whole_name)  # 保存文件
    return file_whole_name  # 返回文件绝对路径


def get_question_keys(message):
    """
    设置一个列表，将信息中的问题关键字提取出来放到列表中
    :param message:
    :return:
    """
    keys = []
    for key in question_dict.keys():  # 遍历问题字典中的所有键
        if key in message.text:
            keys.append(key)
    return keys


def get_questions_pictures_list(target_group_messages):
    """
    遍历每一条群聊信息，获取发票图片及问题关键字列表
    :param target_group_messages: 目标群聊信息
    :return:发票图片及问题关键字列表
    """
    remove_messages = []
    questions_pictures_list = []
    pictures_list = []
    questions_list = []
    if target_group_messages:  # 群聊信息不为空
        # 遍历每一条群聊信息
        for message in target_group_messages:
            if message.type == 'Text':
                questions_list.extend(get_question_keys(message))  # 使用扩展列表的方法向问题关键字列表中添加关键字，添加完成后仍未一个列表
            if message.type == 'Picture':
                if message.file_name.split('.')[-1] != 'gif':
                    pictures_list.append(save_pic_file(message))  # 如果信息类型为图片，则保存图片并添加到列表
            remove_messages.append(message)
        for remove_message in remove_messages:
            target_group_messages.remove(remove_message)  # 清空群信息列表

        questions_list = list(set(questions_list))  # 使用集合删除列表中的重复元素
        questions_pictures_list.append(pictures_list)  # 双列表合成单列表
        questions_pictures_list.append(questions_list)
        return questions_pictures_list


def invoice_bot(bot, group_name):
    """
    将前面的各个步骤（函数）整合成一个大函数，返回发票图片及问题关键字列表
    :param bot: 微信机器人
    :param group_name: 目标群名称
    :return: 发票图片及问题关键字列表
    """
    target_group_messages = get_group_message(bot, group_name)  # 获取目标群聊信息
    questions_pictures_list = get_questions_pictures_list(target_group_messages)  # 保存目标群聊信息中的图片信息
    print(questions_pictures_list)
    return questions_pictures_list


def send_group_message(bot, group_name, message):
    """
    向制定群发送信息
    :param bot:微信机器人
    :param group_name:目标群聊
    :param message:发送的信息
    :return:None
    """
    group = bot.groups().search(group_name)[0]
    print(group)
    group.send_msg(message)


#
# bot = Bot()  # 实例化机器人对象
# group_name = '发票校验'
# group = bot.groups().search(group_name)[0]

# pic_list = pic_list_bot(bot, group_name)

# print('end')
# print('end')