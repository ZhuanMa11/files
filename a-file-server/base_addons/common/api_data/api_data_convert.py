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
import datetime
import os
import urllib

import constants
import dtcloud

PREVIEW_FOLDER_TYPE = "preview_file"
MODEL_FOLDER_TYPE = "model_file"


class CommonApiDataConvert:

    # 返回数据data
    @staticmethod
    def api_page_data_convert_list(obj, pool):
        """
        返回前端想要的字典格式
        @param obj: 数据库查询的结果集
        @param pool: 执行容器
        @return: 返回前端想要的字典格式
        """
        data_list = list()
        if obj != {}:
            for order in obj:
                data_list.append(CommonApiDataConvert.api_data_convert(order, pool))
        return data_list

    @staticmethod
    def api_data_convert(order, pool):
        """
        单条记录的数据转换
        @param order: 单条记录
        @param pool: 容器
        @return: 转换结果
        """
        if 'res.users' == order._name:
            return_info = {
                "unit_type_name": order.sx_unit_management_id.unit_type_id.name,
                "unit_type_id": order.sx_unit_management_id.unit_type_id.id,
            }
            page_column = ['id', 'login', 'sx_unit_management_id', 'user_key', 'account_type_id', 'telephone',
                           "user_status", 'create_date']

            for value in page_column:
                v = 'order.%s' % value
                if type(eval(v)) in [int, float, bool, str, bytes, datetime.datetime]:
                    if type(eval(v)) == datetime.datetime:
                        return_info[value] = str((eval(v)).strftime("%Y-%m-%d"))
                        return_info[value + "_HHMMSS"] = str((eval(v)).strftime("%Y-%m-%d %H:%M:%S"))
                    else:
                        return_info[value] = eval(v) or False
                else:
                    return_info[value] = eval(v).id or ''
                    return_info[value.replace('_id', '_name') if '_id' in value else value + '_name'] = eval(
                        v).name or ''

        elif 'file.library' == order._name:
            view_flag = False
            if order.ext in constants.preview_ext:
                addons_path = dtcloud.tools.config.get('addons_path').split(',')[-1]
                if order.ext in constants.model_ext:
                    path = urllib.parse.unquote(order.view_path).split(MODEL_FOLDER_TYPE, 1)[-1]
                    view_path = addons_path + '/' + MODEL_FOLDER_TYPE + path
                    sdb_path = view_path.replace(view_path.rsplit('.', 1)[-1], 'sdb')
                    if os.path.exists(view_path) and os.path.exists(sdb_path):
                        view_flag = True
                else:
                    path = urllib.parse.unquote(order.view_path).split(PREVIEW_FOLDER_TYPE, 1)[-1]
                    view_path = addons_path + '/' + PREVIEW_FOLDER_TYPE + path
                    if os.path.exists(view_path):
                        view_flag = True
            return_info = {
                "id": order.id or '',
                "name": order.name or '',
                "ext": order.ext or '',
                "full_name": order.name+'.'+order.ext or '',
                "path": order.path or '',
                "size": order.size or '',
                "md5": order.md5 or '',
                "view_path": order.view_path or '',
                "download_path": eval(order.download_path) or '',
                "create_date": order.create_date.strftime("%Y-%m-%d"),
                "create_date_HHMMSS": order.create_date.strftime("%Y-%m-%d %H:%M:%S"),
                "write_date": order.write_date.strftime("%Y-%m-%d"),
                "write_date_HHMMSS": order.write_date.strftime("%Y-%m-%d %H:%M:%S"),
                "view_flag": view_flag
            }
        else:
            return_info = {}
            for value in order._fields.keys():
                if value in ["display_name", "__last_update"]:
                    continue
                v = 'order.%s' % value
                if type(eval(v)) in [bool, str, bytes, datetime.datetime, datetime.date]:
                    if type(eval(v)) == datetime.datetime or type(eval(v)) == datetime.date:
                        return_info[value] = str((eval(v)).strftime("%Y-%m-%d"))
                        return_info[value + "_HHMMSS"] = str((eval(v)).strftime("%Y-%m-%d %H:%M:%S"))
                    else:
                        return_info[value] = eval(v) or ''
                elif type(eval(v)) in [int]:
                    return_info[value] = eval(v) or 0
                elif type(eval(v)) in [float]:
                    return_info[value] = eval(v) or 0.00
                else:
                    if eval(v).id:
                        return_info[value] = eval(v).id or ''
                        if 'name' in eval(v):
                            return_info[value.replace('_id', '_name') if '_id' in value else value + '_name'] = eval(
                                v).name or ''

        return return_info

    @staticmethod
    def get_key_and_value_list(obj: list) -> list:
        """
        返回下拉框key(id)和value(name)值

        :param obj: 数据集
        :return: 下拉框的值
        """
        data_list = list()
        if obj != {}:
            for order in obj:
                data_list.append(CommonApiDataConvert.get_key_and_value(order))
        return data_list

    @staticmethod
    def get_key_and_value(order):
        """
        返回key(id)和value(name)值
        :param order: 单条数据的值
        :return: key(id)和value(name)值
        """
        data_dict = {
            "id": order.id,
            "name": order.name
        }
        return data_dict

    @staticmethod
    def get_key_and_value_distinct_list(obj: list, res_field: str) -> list:
        """
        返回下拉框key(根据类型设定)和value(前端传入的字段的值)值

        :param obj: 数据集
        :param res_field: 前端传入的字段
        :return: 下拉框的值
        """
        dropdown_list = []
        if obj:
            for rec in obj:
                if type(rec[res_field]) in [int, float, bool, str, bytes, datetime.datetime]:
                    value = {
                        "id": rec[res_field],
                        "name": rec[res_field]
                    }
                else:
                    value = {
                        "id": rec[res_field][0],
                        "name": str(rec[res_field][1]),
                    }
                dropdown_list.append(value)
        return dropdown_list
