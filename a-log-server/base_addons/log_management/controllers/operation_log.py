# -*- coding: utf-8 -*-
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# DTCloud v2.0
# QQ: 190066183
# 邮件: 190066183@qq.com
# 手机: 18118160329
# 作者: 'zyf_Flame'
# 公司网址: http://www.dtcloud360.com
# Copyright 中亿丰数字科技有限公司 2012-2022 Flame
# 日期: 2022/11/2
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
from dtcloud import http
from dtcloud.addons.web.controllers.main import Home as Api
from ...common.api_crud.api_create import CommonApiCreate
from ...common.api_crud.api_delete import CommonApiDelete
from ...common.api_crud.api_get import CommonApiGet
from ...common.api_crud.api_update import CommonApiUpdate
from ...common.api_data.api_data_return import CommonApiDataReturn

from ...common.api_wrapper.api_route_wapper import CommonApiRouteWrapper

MODEL = "operation.log"


# noinspection PyTypeChecker

class OperationLogController(Api):

    @CommonApiRouteWrapper.response_json
    @http.route(['/api/v1/operation_log'], type='http', auth="public", methods=['POST'], website=True, csrf=False,
                cors='*')
    def create_operation_log_record(self, **kw: dict) -> dict:
        """
        创建操作日志

        :param kw: 接口入參
        :return: 执行结果''
        """
        kw["model"] = MODEL
        data, code = CommonApiCreate.create_record(kw)
        return CommonApiDataReturn.edit_return_data({"code": code, "data": data})

    @CommonApiRouteWrapper.response_json
    @http.route(['/api/v1/operation_log/<int:res_id>'], type='http', auth="public", methods=['DELETE'], website=True,
                csrf=False, cors='*')
    def delete_operation_log_single_record(self, **kw: dict) -> dict:
        """
        刪除操作日志

        :param kw: 接口入參
        :return: 执行结果
        """
        kw["model"] = MODEL
        data, code = CommonApiDelete.delete_single_record(kw)
        return CommonApiDataReturn.edit_return_data({"code": code, "data": data})

    @CommonApiRouteWrapper.response_json
    @http.route(['/api/v1/operation_log'], type='http', auth="public", methods=['DELETE'], website=True,
                csrf=False, cors='*')
    def delete_operation_log_records(self, **kw: dict) -> dict:
        """
        根据条件列表删除多条操作日志记录

        :param kw: 接口入参
        :return: 数据和消息key
        """
        kw["model"] = MODEL
        data, code = CommonApiDelete.delete_records_by_res_ids(kw)
        return CommonApiDataReturn.edit_return_data({"code": code, "data": data})

    @CommonApiRouteWrapper.response_json
    @http.route(['/api/v1/operation_log/<int:res_id>'], type='http', auth="public", methods=['GET'], website=True,
                csrf=False, cors='*')
    def get_operation_log_single_record(self, **kw: dict) -> dict:
        """
        根据主键获取单条登操作日志记录

        :param kw: 接口入参
        :return: 数据和消息key
        """
        kw["model"] = MODEL
        data, code = CommonApiGet.get_single_record(kw)
        return CommonApiDataReturn.edit_return_data({"code": code, "data": data})

    @CommonApiRouteWrapper.response_json
    @http.route(['/api/v1/operation_log'], type='http', auth="public", methods=['GET'], website=True, cors='*')
    def get_operation_log_records_by_domain(self, **kw: dict) -> dict:
        """
        根据条件获取操作日志记录

        :param kw: 接口入参
        :return: 数据和消息key
        """
        kw["model"] = MODEL
        data, data_count, code = CommonApiGet.get_records_by_domain(kw)
        return CommonApiDataReturn.edit_return_data({"code": code, 'data_count': data_count, "data": data})

    @CommonApiRouteWrapper.response_json
    @http.route(['/api/v1/operation_log/dropdown'], type='http', auth="public", methods=['GET'], website=True,
                csrf=False, cors='*')
    def get_operation_log_key_and_value_list(self, **kw: dict) -> dict:
        """
        获取下拉框列表值，增加或者修改时，下拉框选择（不做distinct）

        :param kw: 接口入参
        :return: 数据和消息key
        """
        kw["model"] = MODEL
        data, code = CommonApiGet.get_key_and_value_list(kw)
        return CommonApiDataReturn.edit_return_data({"code": code, "data": data})

    @CommonApiRouteWrapper.response_json
    @http.route(['/api/v1/operation_log/dropdown/<string:res_field>'], type='http', auth="public", methods=['GET'],
                website=True, csrf=False, cors='*')
    def get_operation_log_key_and_value_distinct_list(self, **kw: dict) -> dict:
        """
        获取下拉框列表值,列表页做筛选（做distinct）

        :param kw: 接口入参
        :return: 数据和消息key
        """
        kw["model"] = MODEL
        data, code = CommonApiGet.get_key_and_value_distinct_list(kw)
        return CommonApiDataReturn.edit_return_data({"code": code, "data": data})

    @CommonApiRouteWrapper.response_json
    @http.route(['/api/v1/operation_log/<int:res_id>'], type='http', auth="public", methods=['PUT'], website=True,
                csrf=False, cors='*')
    def update_operation_log_single_record(self, **kw: dict) -> dict:
        """
        根据主键更新单条操作日志记录

        :param kw: 接口入参
        :return: 数据和消息key
        """
        kw["model"] = MODEL
        data, code = CommonApiUpdate.update_single_record(kw)
        return CommonApiDataReturn.edit_return_data({"code": code, "data": data})

    @CommonApiRouteWrapper.response_json
    @http.route(['/api/v1/operation_log'], type='http', auth="public", methods=['PUT'], website=True,
                csrf=False, cors='*')
    def update_operation_log_records(self, **kw: dict) -> dict:
        """
        根据主键列表更新多条操作日志信息

        :param kw: 接口入参
        :return: 数据和消息key
        """
        kw["model"] = MODEL
        data, code = CommonApiUpdate.update_records_by_res_ids(kw)
        return CommonApiDataReturn.edit_return_data({"code": code, "data": data})
