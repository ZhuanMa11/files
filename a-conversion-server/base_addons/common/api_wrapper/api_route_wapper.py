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
import functools
import json

from base_addons.common.api_message.message_info import CommonMessageInfo


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
                message = CommonMessageInfo.code_match_message(7)
                param = {"message": message, "data": {}, 'error': str(e)}
                return json.dumps(param)
        return wrapper
