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
from base_addons.common.api_data.api_data_convert import CommonApiDataConvert
from base_addons.common.api_data.api_data_domain import CommonApiDataDomain
from dtcloud.addons.web.controllers.main import Home as Api


class CommonApiGet(Api):

    @staticmethod
    def get_single_record(kw: dict):
        """
        根据主键获取单条信息

        :param kw: 接口入参
        :return: 数据和消息key
        """
        pool = request.env
        uid = kw.get('uid')
        model = kw.get('model')
        res_id = kw.get('res_id')
        access_token = kw.get('access_token')
        record = pool[model].sudo().with_user(2).browse(int(res_id))
        data_list = CommonApiDataConvert.api_page_data_convert_list(record)
        return data_list, 2

    @staticmethod
    def get_records_by_domain(kw: dict):
        """
        根据条件获取多条记录

        :param kw: 接口入参
        :return: 数据和消息key
        """
        pool = request.env
        uid = kw.get('uid', 2)
        model = kw.get('model')
        page = kw.get('page', 0)
        limit = kw.get('limit', 0)
        domain = kw.get('domain', str(list()))
        order = kw.get('order', 'id desc')
        # todo 改写domain
        domain = CommonApiDataDomain.edit_domain(domain)
        if page and limit:
            records = pool[model].sudo().with_user(2).search(domain, limit=int(limit), offset=int(page) * int(limit),
                                                               order=order)
        else:
            records = pool[model].sudo().with_user(2).search(domain, order=order)
        data_count = pool[model].sudo().with_user(2).search_count(domain)
        data_list = CommonApiDataConvert.api_page_data_convert_list(records)
        return data_list, data_count, 2

    @staticmethod
    def get_key_and_value_list(kw: dict):
        """
        获取下拉框列表值，增加或者修改时，下拉框选择，子父级联动子集选择（不做distinct）

        :param kw: 接口入参
        :return: 数据和消息key
        """
        pool = request.env
        uid = kw.get('uid')
        model = kw.get('model')
        domain = kw.get('domain', str(list()))
        order = kw.get('order', 'id desc')
        # todo 改写domain
        domain = CommonApiDataDomain.edit_domain(domain)
        records = pool[model].sudo().with_user(2).search(domain, order=order)
        data_list = CommonApiDataConvert.get_key_and_value_list(records)
        return data_list, 2

    @staticmethod
    def get_key_and_value_distinct_list(kw: dict):
        """
        获取下拉框列表值,列表页做筛选（做distinct）

        :param kw: 接口入参
        :return: 数据和消息key
        """
        pool = request.env
        uid = kw.get('uid')
        model = kw.get('model')
        domain = kw.get('domain', str(list()))
        # 页面distinct字段
        res_field = kw.get('res_field')
        order = kw.get('order', 'id desc')
        # todo 改写domain
        domain = CommonApiDataDomain.edit_domain(domain)
        records = pool[model].sudo().with_user(2).read_group(domain, [res_field], [res_field], orderby=order)
        data_list = CommonApiDataConvert.get_key_and_value_distinct_list(records, res_field)
        return data_list, 2
