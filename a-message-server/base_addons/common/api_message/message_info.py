# -*- coding: utf-8 -*-
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# DTCloud v2.0
# QQ: 190066183
# 邮件: 190066183@qq.com
# 手机: 18118160329
# 作者: 'zyf_KyoRyu'
# 公司网址: http://www.dtcloud360.com
# Copyright 中亿丰数字科技有限公司 2012-2022 KyoRyu
# 日期: 2022/7/29
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

# 自定义的message，获取data之后自己重写
# error code<0
# success 0 <=code< 99
# message 100 <=code< 199
# info 400 <=code< 499
from dtcloud.http import request


# noinspection PyIncorrectDocstring

class CommonMessageInfo:

    @classmethod
    def code_match_message(cls, code: int):
        """
        上传文件主函数

        :param kw: 接口入参
        :return: 数据和消息key
        """
        pool = request.env
        info = pool['message.management'].sudo().search([('id', '=', code)])
        if info:
            message_dict = {"flag": info.flag, "content": info.name, "next_operation": info.next_operation}
            return message_dict
        return False
