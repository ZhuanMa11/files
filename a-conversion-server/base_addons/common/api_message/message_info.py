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

import json
import requests
import dtcloud


# noinspection PyIncorrectDocstring

class CommonMessageInfo:

    @classmethod
    def code_match_message(cls, code: int) -> dict:
        """
        校验是否有权限请求接口

        :param code: 编码
        :return: message_dict or {}
        """
        message_url = dtcloud.tools.config.get('message_url')
        response = requests.get('%s/api/v1/message_management/%s' % (message_url, code), data={})
        info = json.loads(response.text)
        if info["message"]['flag'] == 'success':
            message_dict = {"flag": info["data"][0]['flag'], "content": info["data"][0]['name'],
                            "next_operation": info["data"][0]['next_operation']}
            return message_dict
        return {}
