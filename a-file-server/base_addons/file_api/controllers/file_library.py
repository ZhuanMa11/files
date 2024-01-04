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
from dtcloud import http
from dtcloud.addons.web.controllers.main import Home as Api
from ..service.file_library import FileApiService
from ...common.api_crud.api_create import CommonApiCreate
from ...common.api_crud.api_delete import CommonApiDelete
from ...common.api_crud.api_get import CommonApiGet
from ...common.api_crud.api_update import CommonApiUpdate
from ...common.api_data.api_data_return import CommonApiDataReturn

from ...common.api_wrapper.api_route_wapper import CommonApiRouteWrapper

MODEL = "file.library"


# noinspection PyTypeChecker

class FileLibraryController(Api):

    @CommonApiRouteWrapper.response_json
    @http.route(['/api/v1/file_library'], type='http', auth="public", methods=['POST'], website=True, csrf=False,
                cors='*')
    def create_file_library_record(self, **kw: dict) -> dict:
        """
        创建系统文档

        :param kw: 接口入參
        :return: 执行结果''
        """
        kw["model"] = MODEL
        data, code = CommonApiCreate.create_record(kw)
        return CommonApiDataReturn.edit_return_data({"code": code, "data": data})

    @CommonApiRouteWrapper.response_json
    @http.route(['/api/v1/file_library/<int:res_id>'], type='http', auth="public", methods=['DELETE'], website=True,
                csrf=False, cors='*')
    def delete_file_library_single_record(self, **kw: dict) -> dict:
        """
        刪除系统文档

        :param kw: 接口入參
        :return: 执行结果
        """
        kw["model"] = MODEL
        data, code = CommonApiDelete.delete_single_record(kw)
        return CommonApiDataReturn.edit_return_data({"code": code, "data": data})

    @CommonApiRouteWrapper.response_json
    @http.route(['/api/v1/file_library'], type='http', auth="public", methods=['DELETE'], website=True,
                csrf=False, cors='*')
    def delete_file_library_records(self, **kw: dict) -> dict:
        """
        根据条件列表删除多条系统文档记录

        :param kw: 接口入参
        :return: 数据和消息key
        """
        kw["model"] = MODEL
        data, code = CommonApiDelete.delete_records_by_res_ids(kw)
        return CommonApiDataReturn.edit_return_data({"code": code, "data": data})

    @CommonApiRouteWrapper.response_json
    @http.route(['/api/v1/file_library/<int:res_id>'], type='http', auth="public", methods=['GET'], website=True,
                csrf=False, cors='*')
    def get_file_library_single_record(self, **kw: dict) -> dict:
        """
        根据主键获取单条登系统文档记录

        :param kw: 接口入参
        :return: 数据和消息key
        """
        kw["model"] = MODEL
        kw["uid"] = 2
        data, code = CommonApiGet.get_single_record(kw)
        return CommonApiDataReturn.edit_return_data({"code": code, "data": data})

    @CommonApiRouteWrapper.response_json
    @http.route(['/api/v1/file_library'], type='http', auth="public", methods=['GET'], website=True, cors='*')
    def get_file_library_records_by_domain(self, **kw: dict) -> dict:
        """
        根据条件获取系统文档记录

        :param kw: 接口入参
        :return: 数据和消息key
        """
        kw["model"] = MODEL
        data, code = CommonApiGet.get_records_by_domain(kw)
        return CommonApiDataReturn.edit_return_data({"code": code, "data": data})



    @CommonApiRouteWrapper.response_json
    @http.route(['/api/v1/file_library/dropdown'], type='http', auth="public", methods=['GET'], website=True,
                csrf=False, cors='*')
    def get_file_library_key_and_value_list(self, **kw: dict) -> dict:
        """
        获取下拉框列表值，增加或者修改时，下拉框选择（不做distinct）

        :param kw: 接口入参
        :return: 数据和消息key
        """
        kw["model"] = MODEL
        data, code = CommonApiGet.get_key_and_value_list(kw)
        return CommonApiDataReturn.edit_return_data({"code": code, "data": data})

    @CommonApiRouteWrapper.response_json
    @http.route(['/api/v1/file_library/dropdown/<string:res_field>'], type='http', auth="public", methods=['GET'],
                website=True, csrf=False, cors='*')
    def get_file_library_key_and_value_distinct_list(self, **kw: dict) -> dict:
        """
        获取下拉框列表值,列表页做筛选（做distinct）

        :param kw: 接口入参
        :return: 数据和消息key
        """
        kw["model"] = MODEL
        data, code = CommonApiGet.get_key_and_value_distinct_list(kw)
        return CommonApiDataReturn.edit_return_data({"code": code, "data": data})

    @CommonApiRouteWrapper.response_json
    @http.route(['/api/v1/file_library/<int:res_id>'], type='http', auth="public", methods=['PUT'], website=True,
                csrf=False, cors='*')
    def update_file_library_single_record(self, **kw: dict) -> dict:
        """
        根据主键更新单条系统文档记录

        :param kw: 接口入参
        :return: 数据和消息key
        """
        kw["model"] = MODEL
        data, code = CommonApiUpdate.update_single_record(kw)
        return CommonApiDataReturn.edit_return_data({"code": code, "data": data})

    @CommonApiRouteWrapper.response_json
    @http.route(['/api/v1/file_library'], type='http', auth="public", methods=['PUT'], website=True,
                csrf=False, cors='*')
    def update_file_library_records(self, **kw: dict) -> dict:
        """
        根据主键列表更新多条系统文档信息

        :param kw: 接口入参
        :return: 数据和消息key
        """
        kw["model"] = MODEL
        data, code = CommonApiUpdate.update_records_by_res_ids(kw)
        return CommonApiDataReturn.edit_return_data({"code": code, "data": data})

    @CommonApiRouteWrapper.response_json
    @http.route(['/api/v1/upload'], type='http', auth="public", methods=['POST', 'OPTIONS'], website=True,
                csrf=False, cors='*')
    def upload_file(self, **kw: dict) -> dict:
        """
        上传文件

        :param kw: 接口入参
        :return: 上传结果 2成功 5失败:未上传文件
        """
        kw["model"] = MODEL
        data, code = FileApiService.upload_file(kw)
        return CommonApiDataReturn.edit_return_data({"code": code, "data": data})

    @http.route(['/api/v1/download/<int:res_id>'], type='http', auth="public", methods=['GET'], website=True,
                csrf=False, cors='*')
    def download_file(self, **kw: dict) -> dict:
        """
        下载指定文件

        :param kw: 接口入参
        :return: 下载流
        """
        kw["model"] = MODEL
        return FileApiService.download_file(kw)

    @http.route(['/api/v1/stream_download/<int:res_id>'], type='http', auth="public", methods=['GET'], website=True,
                csrf=False, cors='*')
    def stream_download_file(self, **kw: dict) -> dict:
        """
        流式下载指定文件

        :param kw: 接口入参
        :return: 下载流
        """
        kw["model"] = MODEL
        return FileApiService.stream_download_file(kw)

    @CommonApiRouteWrapper.response_json
    @http.route(['/api/v1/check_preview/<int:res_id>'], type='http', auth="public", methods=['GET'], website=True,
                csrf=False, cors='*')
    def check_preview_file(self, **kw: dict) -> dict:
        """
        检查指定文件是否可以预览

        :param kw: 接口入参
        :return: {code:7/8} 7:可以预览，8:不可以预览
        """
        kw["model"] = MODEL
        code = FileApiService.check_preview_file(kw)
        return CommonApiDataReturn.edit_return_data({"code": code})

    @CommonApiRouteWrapper.response_json
    @http.route(['/api/v1/batch_download'], type='http', auth="public", methods=['GET'], website=True,
                csrf=False, cors='*')
    def batch_download_file(self, **kw: dict) -> dict:
        """
        批量下载（按照指定文件目录下载）

        :param kw: 接口入参
        :return:
        """
        kw["model"] = MODEL
        data, code, message = FileApiService.batch_download_file(kw)
        return CommonApiDataReturn.edit_return_data({"code": code, 'message': message, 'data': data})

    @CommonApiRouteWrapper.response_json
    @http.route(['/api/v1/parse_model'], type='http', auth="public", methods=['GET'], website=True,
                csrf=False, cors='*')
    def parse_model(self, **kw: dict) -> dict:
        """
        获取构建tree

        :param kw: 接口入参
        :return:
        """
        kw["model"] = MODEL
        data, code, message = FileApiService.parse_model(kw)
        return CommonApiDataReturn.edit_return_data({"code": code, 'message': message, 'data': data})

    @CommonApiRouteWrapper.response_json
    @http.route(['/api/v1/build_properties'], type='http', auth="public", methods=['GET'], website=True,
                csrf=False, cors='*')
    def build_properties(self, **kw: dict) -> dict:
        """
        获取模型构建属性

        :param kw: 接口入参
        :return:
        """
        kw["model"] = MODEL
        data, code = FileApiService.get_build_properties(kw)
        return CommonApiDataReturn.edit_return_data({"code": code, 'data': data})

    @CommonApiRouteWrapper.response_json
    @http.route(['/api/v1/PC_build_properties'], type='http', auth="public", methods=['GET'], website=True,
                csrf=False, cors='*')
    def pc_build_properties(self, **kw: dict) -> dict:
        """
        获取模型所有PC构建属性

        :param kw: 接口入参
        :return:
        """
        kw["model"] = MODEL
        data, code = FileApiService.get_pc_build_properties(kw)
        return CommonApiDataReturn.edit_return_data({"code": code, 'data': data})


