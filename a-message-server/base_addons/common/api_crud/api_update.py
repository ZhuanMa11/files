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


class CommonApiUpdate(Api):

    @classmethod
    def update_single_record(cls, kw: dict):
        """
        根据主键更新单条信息

        :param kw: 接口入参
        :return: 数据和消息key
        """
        pool = request.env
        uid = kw.get('uid')
        model = kw.get('model')
        res_id = kw.get('res_id')
        data = json.loads(kw.get('data'))
        res = cls.update_record_by_id(model, pool, uid, res_id, data)
        return res, 5

    @classmethod
    def update_records_by_res_ids(cls, kw: dict):
        """
        根据主键列表更新多条信息

        :param kw: 接口入参
        :return: 数据和消息key
        """
        pool = request.env
        uid = kw.get('uid')
        model = kw.get('model')
        res_ids = eval(kw.get('res_ids'))
        data = json.loads(kw.get('data'))
        for res_id in res_ids:
            cls.update_record_by_id(model, pool, uid, res_id, data)
        return True, 5

    @staticmethod
    def update_record_by_id(model: str, pool, uid: str, res_id: str, data: dict):
        """
        根据id更新单条记录

        :param model: 实体
        :param pool: 容器
        :param uid: 用户id
        :param res_id: 记录id
        :param data: 更新信息
        """
        record = pool[model].sudo().with_user(2).search([('id', '=', int(res_id))])
        return record.write(data) if record else False

