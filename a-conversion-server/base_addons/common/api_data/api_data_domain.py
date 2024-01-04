# -*- coding: utf-8 -*-
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# DTCloud v2.0
# QQ: 190066183
# 邮件: 190066183@qq.com
# 手机: 18118160329
# 作者: 'zyf_KyoRyu'
# 公司网址: http://www.dtcloud360.com
# Copyright 中亿丰数字科技有限公司 2012-2022 KyoRyu
# 日期: 2022/10/18
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
import ast

from dtcloud.osv import expression


class CommonApiDataDomain:

    @staticmethod
    def edit_domain(domain: str) -> list:
        """
        编辑前端传入的查询条件

        :param domain: 查询条件
        :return: 后端编辑后的值
        """
        domain = eval(domain)
        return domain  # 各查询条件用and拼接

    @staticmethod
    def api_page_domain(textbox_search, dropdown_list_search, search, start_time, end_time, search_domain):
        """拼接查询条件 各个条件间用and search的条件用or
        @param textbox_search: textbox框入力的查询条件
        @param dropdown_list_search: 下拉框的查询条件
        @param search: 搜索框查询条件
        @param start_time: 开始时间
        @param end_time: 结束时间
        @param search_domain: 树节点id
        @return: 拼接的查询条件
        """
        domains = []
        if textbox_search:  # textbox框入力的查询条件
            dic = ast.literal_eval(textbox_search)
            search_keys = dic.keys()
            subdomains = []
            for key in search_keys:
                if dic[key]:
                    subdomains.append([(key, "ilike", dic[key])])
                else:
                    continue
            domains.append(expression.AND(subdomains))

        if dropdown_list_search:  # 下拉框的查询条件
            dic = ast.literal_eval(dropdown_list_search)
            search_keys = dic.keys()
            subdomains = []
            for key in search_keys:
                if dic[key]:
                    subdomains.append([(key, "=", dic[key])])
                    if dic[key] == '0':
                        subdomains.append([(key, "=", False)])
                else:
                    continue
            domains.append(expression.AND(subdomains))

        if search:  # 搜索框查询条件
            dic = ast.literal_eval(search)
            search_keys = dic.keys()
            subdomains = []
            for key in search_keys:
                search_column = key.split("||")
                for search_value in dic[key].split(" "):
                    if not search_value:
                        continue
                    for search_key in search_column:
                        subdomains.append([(search_key, 'ilike', search_value)])
            domains.append(expression.AND(subdomains))  # 条件用or拼接

        if start_time:  # 开始时间 和结束时间
            subdomains = [
                [('create_date', '>=', start_time)],
            ]
            if end_time:
                subdomains.append([('create_date', '<=', end_time)])
            domains.append(expression.AND(subdomains))

        if search_domain:
            dic = ast.literal_eval(search_domain)
            search_keys = dic.keys()
            subdomains = []
            for key in search_keys:
                subdomains.append([(key, "=", dic[key])])
            domains.append(expression.AND(subdomains))
        return expression.AND(domains)  # 各查询条件用and拼接
