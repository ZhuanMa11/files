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
from dtcloud.http import request
from dtcloud.addons.web.controllers.main import Home as Api


class CommonApiDelete(Api):

    @classmethod
    def delete_single_record(cls, kw: dict):
        """
        根据主键删除单条记录

        :param kw: 接口入参
        :return: 数据和消息key
        """
        pool = request.env
        uid = kw.get('uid')
        model = kw.get('model')
        res_id = kw.get('res_id')
        cls.delete_record_by_id(model, pool, uid, res_id)
        return True, 5

    @classmethod
    def delete_records_by_res_ids(cls, kw: dict):
        """
        根据主键列表删除多条记录

        :param kw: 接口入参
        :return: 数据和消息key
        """
        pool = request.env
        uid = kw.get('uid')
        model = kw.get('model')
        res_ids = eval(kw.get('res_ids'))
        for res_id in res_ids:
            cls.delete_record_by_id(model, pool, uid, res_id)
        return True, 5

    @staticmethod
    def delete_record_by_id(model: str, pool, uid: str, res_id: str):
        """
        根据id删除单条记录

        :param model: 实体
        :param pool: 容器
        :param uid: 用户id
        :param res_id: 记录id
        """
        record = pool[model].sudo().with_user(2).search([('id', '=', int(res_id))])
        if record:
            # 查询关联的文件，删除
            res_file_domain = list()
            res_file_domain.append(("res_model", "=", model))
            res_file_domain.append(("res_id", "=", res_id))
            pool["business.file.res"].sudo().with_user(2).search(res_file_domain).unlink()
            record.unlink()
