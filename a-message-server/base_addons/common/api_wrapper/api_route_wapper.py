# -*-coding:utf-8-*-
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# DTCloud v2.0
# QQ: 190066183
# 邮件: 190066183@qq.com
# 手机: 18118160329
# 作者: 'zyf_KyoRyu'
# 公司网址: http://www.dtcloud360.com
# Copyright 中亿丰数字科技有限公司 2012-2022 KyoRyu
# 日期: 2022/10/21
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
import datetime
import functools
import json
import threading
import traceback

import requests

import dtcloud
from base_addons.common.api_message.message_info import CommonMessageInfo
from dtcloud.http import request


class CommonApiRouteWrapper:

    @classmethod
    def response_json(cls, func):
        """
        方法请求时，返回json序列化

        :param func: 调用此装饰器的方法
        :return: 执行结果
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                param = func(*args, **kwargs)
                return param
            except Exception as e:
                # TODO 错误日志
                message = CommonMessageInfo.code_match_message(5)
                param = {"message": message, "data": {}}
                return json.dumps(param)

        return wrapper

    @staticmethod
    def _check_access_token_request(access_token: str) -> bool:
        """
        校验是否有权限请求接口

        :param access_token: 用户唯一识别码
        :return: True or False
        """
        post_data = {
            "access_token": access_token,
        }
        main_server_url = dtcloud.tools.config.get('main_server_url')
        response = requests.get('%s/api/v1/access_token' % main_server_url, data=post_data)
        info = json.loads(response.text)
        if info["code"] == 1:
            return True
        return False
