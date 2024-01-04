# -*- coding: utf-8 -*-
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# DTCloud v2.0
# QQ: 190066183
# 邮件: 190066183@qq.com
# 手机: 18118160329
# 作者: 'zyf_KyoRyu'
# 公司网址: http://www.dtcloud360.com
# Copyright 中亿丰数字科技有限公司 2012-2022 KyoRyu
# 日期: 2022/11/30
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
import json

from base_addons.common.api_message.message_info import CommonMessageInfo


class CommonApiDataReturn:

    @classmethod
    def edit_return_data(cls, param):
        """
        编辑前端传入的查询条件

        :param param: 查询条件
        :return: 返回的值
        """
        message_dict = CommonMessageInfo.code_match_message(param['code'])
        if 'message' in param:
            message_dict['content'] = message_dict['content'] % param['message']
        else:
            message_dict['content'] = message_dict['content'].replace('%s', '')
        param['message'] = message_dict
        del [param['code']]
        return json.dumps(param)