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

from dtcloud.addons.web.controllers.main import Home as Api
from dtcloud.http import request


class CommonApiCreate(Api):

    @classmethod
    def create_record(cls, kw):
        """
        创建单条记录

        :param kw:接口入参
        """
        pool = request.env
        uid = kw.get('uid')
        model = kw.get('model')
        data = json.loads(kw.get('data'))
        record = cls.create_single_record(pool, model, uid, data)
        return record.id, 5

    @staticmethod
    def create_single_record(pool, model: str, uid: str, data: dict):
        """
        创建一条记录

        :param pool: 容器
        :param model: 实体
        :param uid: 用户id
        :param data: 创建信息
        :return: 创建的实体
        """
        return pool[model].sudo().with_user(2).create(data)
