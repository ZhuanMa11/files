import json

from base_addons.common.api_data.api_data_return import CommonApiDataReturn
from dtcloud import http
from dtcloud.addons.web.controllers.main import Home as Api
from base_addons.common.api_crud.api_create import CommonApiCreate
from base_addons.common.api_crud.api_delete import CommonApiDelete
from base_addons.common.api_crud.api_get import CommonApiGet
from base_addons.common.api_crud.api_update import CommonApiUpdate
from base_addons.common.api_wrapper.api_route_wapper import CommonApiRouteWrapper
from dtcloud.http import request

MODEL = "conversion.record"


# noinspection PyTypeChecker

class ConversionRecordController(Api):

    @CommonApiRouteWrapper.response_json
    @http.route(['/api/v1/conversion_record'], type='http', auth="public", methods=['POST'], website=True, csrf=False,
                cors='*')
    def create_conversion_record_record(self, **kw: dict) -> dict:
        """
        创建转换记录

        :param kw: 接口入參
        :return: 执行结果''
        """
        kw["model"] = MODEL
        data, code = CommonApiCreate.create_record(kw)
        return CommonApiDataReturn.edit_return_data({"code": code, "data": data})

    @CommonApiRouteWrapper.response_json
    @http.route(['/api/v1/conversion_record/<int:res_id>'], type='http', auth="public", methods=['DELETE'],
                website=True,
                csrf=False, cors='*')
    def delete_conversion_record_single_record(self, **kw: dict) -> dict:
        """
        刪除转换记录

        :param kw: 接口入參
        :return: 执行结果
        """
        kw["model"] = MODEL
        data, code = CommonApiDelete.delete_single_record(kw)
        return CommonApiDataReturn.edit_return_data({"code": code, "data": data})

    @CommonApiRouteWrapper.response_json
    @http.route(['/api/v1/conversion_record'], type='http', auth="public", methods=['DELETE'], website=True,
                csrf=False, cors='*')
    def delete_conversion_record_records(self, **kw: dict) -> dict:
        """
        根据条件列表删除多条转换记录记录

        :param kw: 接口入参
        :return: 数据和消息key
        """
        kw["model"] = MODEL
        data, code = CommonApiDelete.delete_records_by_res_ids(kw)
        return CommonApiDataReturn.edit_return_data({"code": code, "data": data})

    @CommonApiRouteWrapper.response_json
    @http.route(['/api/v1/conversion_record/<int:res_id>'], type='http', auth="public", methods=['GET'], website=True,
                csrf=False, cors='*')
    def get_conversion_record_single_record(self, **kw: dict) -> dict:
        """
        根据主键获取单条登转换记录记录

        :param kw: 接口入参
        :return: 数据和消息key
        """
        kw["model"] = MODEL
        data, code = CommonApiGet.get_single_record(kw)
        return CommonApiDataReturn.edit_return_data({"code": code, "data": data})

    @CommonApiRouteWrapper.response_json
    @http.route(['/api/v1/conversion_record'], type='http', auth="public", methods=['GET'], website=True, cors='*')
    def get_conversion_record_records_by_domain(self, **kw: dict) -> dict:
        """
        根据条件获取转换记录记录

        :param kw: 接口入参
        :return: 数据和消息key
        """
        kw["model"] = MODEL
        data, data_count, code = CommonApiGet.get_records_by_domain(kw)
        return CommonApiDataReturn.edit_return_data({"code": code, "data_count": data_count, "data": data})

    @CommonApiRouteWrapper.response_json
    @http.route(['/api/v1/conversion_record/dropdown'], type='http', auth="public", methods=['GET'], website=True,
                csrf=False, cors='*')
    def get_conversion_record_key_and_value_list(self, **kw: dict) -> dict:
        """
        获取下拉框列表值，增加或者修改时，下拉框选择（不做distinct）

        :param kw: 接口入参
        :return: 数据和消息key
        """
        kw["model"] = MODEL
        data, code = CommonApiGet.get_key_and_value_list(kw)
        return CommonApiDataReturn.edit_return_data({"code": code, "data": data})

    @CommonApiRouteWrapper.response_json
    @http.route(['/api/v1/conversion_record/dropdown/<string:res_field>'], type='http', auth="public", methods=['GET'],
                website=True, csrf=False, cors='*')
    def get_conversion_record_key_and_value_distinct_list(self, **kw: dict) -> dict:
        """
        获取下拉框列表值,列表页做筛选（做distinct）

        :param kw: 接口入参
        :return: 数据和消息key
        """
        kw["model"] = MODEL
        data, code = CommonApiGet.get_key_and_value_distinct_list(kw)
        return CommonApiDataReturn.edit_return_data({"code": code, "data": data})

    @CommonApiRouteWrapper.response_json
    @http.route(['/api/v1/conversion_record/<int:res_id>'], type='http', auth="public", methods=['PUT'], website=True,
                csrf=False, cors='*')
    def update_conversion_record_single_record(self, **kw: dict) -> dict:
        """
        根据主键更新单条转换记录记录

        :param kw: 接口入参
        :return: 数据和消息key
        """
        kw["model"] = MODEL
        data, code = CommonApiUpdate.update_single_record(kw)
        return CommonApiDataReturn.edit_return_data({"code": code, "data": data})

    @CommonApiRouteWrapper.response_json
    @http.route(['/api/v1/conversion_record'], type='http', auth="public", methods=['PUT'], website=True,
                csrf=False, cors='*')
    def update_conversion_record_records(self, **kw: dict) -> dict:
        """
        根据主键列表更新多条转换记录信息

        :param kw: 接口入参
        :return: 数据和消息key
        """
        kw["model"] = MODEL
        data, code = CommonApiUpdate.update_records_by_res_ids(kw)
        return CommonApiDataReturn.edit_return_data({"code": code, "data": data})

    @http.route(['/api/convert/v1/get_conversion_count_no_ak'], type='http', auth="public", methods=['GET'],
                website=True,
                csrf=False, cors='*')
    def get_conversion_count_no_ak(self, **kw: dict) -> dict:
        """

        :param kw: 接口入参
        :return: 数据和消息key
        """
        pool = request.env
        count = pool[MODEL].sudo().search_count([])
        return json.dumps({"count": count, "message": {"flag": "success"}})


    @http.route(['/api/convert/v1/get_conversion_record_no_ak'], type='http', auth="public", methods=['GET'],
                website=True, cors='*')
    def get_conversion_record_no_ak(self, **kw: dict) -> dict:
        """
        根据条件获取转换记录记录

        :param kw: 接口入参
        :return: 数据和消息key
        """

        req_dict = dict()
        pool = request.env
        pool.cr.execute(
            "select to_date(create_date::text,'yyyy-mm-dd'),COUNT(id) FROM conversion_record GROUP BY to_date(create_date::text,'yyyy-mm-dd')"
        )
        records = pool.cr.fetchall()

        for record in records:
            req_dict[str(record[0])] = record[1]

        return json.dumps(req_dict)
