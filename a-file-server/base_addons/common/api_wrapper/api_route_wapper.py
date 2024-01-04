# -*-coding:utf-8-*-
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# DTCloud v2.0
# QQ: 190066183
# 邮件: 190066183@qq.com
# 手机: 18118160329
# 作者: 'zyf_KyoRyu'
# 公司网址: http://www.dtcloud360.com
# Copyright 中亿丰数字科技有限公司 2012-2022 KyoRyu
# 日期: 2022/10/21
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
import datetime
import functools
import json
import threading
import traceback
from IPy import IP

import requests

import dtcloud
from base_addons.common.api_message.message_info import CommonMessageInfo
from dtcloud.http import request

METHOD_TO_OPERATION_TYPE = {
    'POST': "创建",
    'GET': "查询",
    'PUT': "更新",
    'DELETE': "删除",
}


class CommonApiRouteWrapper:

    @classmethod
    def access_token_check(cls, func):
        """
        方法请求时，访问权限验证

        :param func: 调用此装饰器的方法
        :return: 执行结果
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            uid = kwargs.get('uid')
            access_token = kwargs.get('access_token')
            pool = request.env
            user = pool['res.users'].sudo().browse(int(uid)).login
            if not cls._uid_not_exist(uid, pool):
                message = CommonMessageInfo.code_match_message(3)
                param = {"message": message, "data": {}}
                return json.dumps(param)
            if not cls._access_token_check(pool, access_token):
                message = CommonMessageInfo.code_match_message(3)
                param = {"message": message, "data": {}}
                return json.dumps(param)
            try:
                operation_start_time = datetime.datetime.now()
                param = func(*args, **kwargs)
                message_dict = CommonMessageInfo.code_match_message(param['code'])
                if 'message' in param:
                    message_dict['content'] = message_dict['content'] % param['message']
                else:
                    message_dict['content'] = message_dict['content'].replace('%s', '')
                param['message'] = message_dict
                del [param['code']]
                operation_end_time = datetime.datetime.now()
                cls._operate_log(operation_start_time, operation_end_time, uid, user, param)
                return json.dumps(param)
            except Exception as e:
                # TODO 错误日志
                error_details = traceback.format_exc()
                cls._operate_error_log(uid, user, error_details, func)
                message = CommonMessageInfo.code_match_message(5)
                param = {"message": message, "data": {}}
                return json.dumps(param)

        return wrapper

    @classmethod
    def response_json(cls, func):
        """
        方法请求时，返回json序列化

        :param func: 调用此装饰器的方法
        :return: 执行结果
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                # environ = request.httprequest.headers.environ
                # ip = environ.get('REMOTE_ADDR')
                # if cls.public_ip(ip):
                #     access_token = kwargs.get('access_token')
                #     if not cls._check_access_token_request(access_token):
                #         message_dict = CommonMessageInfo.code_match_message(6)
                #         message_dict['content'] = message_dict['content'] % '您没有访问服务的权限，请与管理员联系'
                #         return json.dumps({'message': message_dict})
                param = func(*args, **kwargs)
                return param
            except Exception as e:
                # TODO 错误日志
                message = CommonMessageInfo.code_match_message(7)
                param = {"message": message, "data": {}, 'error': str(e)}
                return json.dumps(param)

        return wrapper

    @classmethod
    def public_ip(cls, ip):
        """
        判断ip 是否是公网ip
        :param ip:
        :return:
        """
        if cls.check_value(ip):
            if IP(ip).iptype() is 'PUBLIC':
                return True
            return False
        return False

    @classmethod
    def check_value(cls, ipaddr):

        '''
        检查IP是否合法
        :param ipaddr:  string
        :return True
        '''
        addr = ipaddr.strip().split('.')
        if len(addr) != 4:
            return False
        for i in range(4):
            try:
                addr[i] = int(addr[i])
            except:
                return False
            if addr[i] <= 255 and addr[i] >= 0:
                pass
            else:
                return False
            i += 1
        else:
            return True

    @staticmethod
    def _check_access_token_request(access_token: str) -> bool:
        """
        校验是否有权限请求接口

        :param access_token: 用户唯一识别码
        :return: True or False
        """
        post_data = {
            "access_token": access_token,
        }
        main_server_url = dtcloud.tools.config.get('main_server_url')
        response = requests.get('%s/api/v1/access_token' % main_server_url, data=post_data)
        info = json.loads(response.text)
        if info["code"] == 1:
            return True
        return False

    @classmethod
    def _uid_not_exist(cls, uid: str, pool) -> bool:
        """
        判断当前请求用户是否存在

        :param uid: 用户ID
        :param pool: 容器
        :return: 判断结果 False不存在 True存在
        """
        if not uid or uid == 'null':
            return False
        user = pool['res.users'].sudo().search([('id', '=', int(uid))], limit=1)
        if not user:
            return False
        return True

    @classmethod
    def _access_token_check(cls, pool, access_token: str) -> bool:
        """
        判断token是否过期

        :param pool: 容器
        :param access_token: token的值
        :return: 判断结果 False已过期 True未过期
        """
        dt_cloud_token = pool['access.token'].sudo().search([('access_token', '=', access_token)], order="id desc",
                                                            limit=1)
        if not dt_cloud_token:
            return False
        else:
            now_datetime = datetime.datetime.now()
            if dt_cloud_token.token_date > now_datetime:
                return True
            else:
                return False

    @classmethod
    def _operate_error_log(cls, uid: str, user: str, error_details: str, func):
        """
        操作错误日志

        :param uid: 操作人员id
        :param user: 操作人员账号
        :param error_details: 错误详情
        :param func: 方法
        """
        environ = request.httprequest.headers.environ
        request_route = environ.get('REQUEST_URI', '')
        request_mode = environ.get('REQUEST_METHOD', '')
        operation_object = request_route.replace('/api/v1', '')
        if request_mode == 'POST' and operation_object == '/upload':
            operation_type = '上传'
        else:
            operation_type = METHOD_TO_OPERATION_TYPE[request_mode]
        error_function = func.__name__
        error_path = func.__module__
        error_details = error_details
        request_params = str(request.params)
        threading_3 = threading.Thread(target=cls._request_error_log_serve, args=(
            request_route, request_mode, operation_type, operation_object, uid, user, error_function, error_path,
            error_details, request_params))
        threading_3.start()

    @classmethod
    def _request_error_log_serve(cls, request_route: str, request_mode: str, operation_type: str, operation_object: str,
                                 uid: str, user: str, error_function: str, error_path: str, error_details: str,
                                 request_params: str):
        """
        请求log服务生成错误日志

        :param request_route: 请求路由
        :param request_mode: 请求方式
        :param operation_type: 操作类型
        :param operation_object: 操作对象
        :param uid: 操作人员id
        :param user: 操作人员账号
        :param error_function: 错误方法
        :param error_path: 错误路径
        :param error_details: 错误详情
        :param request_params: 请求
        :return:
        """
        try:
            pyload_data = {
                'request_route': request_route,
                'request_mode': request_mode,
                'operation_type': operation_type,
                'operation_object': operation_object,
                'operator': ','.join([uid, user]),
                'error_function': error_function,
                'error_path': error_path,
                'error_details': error_details,
                'request': request_params
            }
            post_data = {
                "data": json.dumps(pyload_data),
                "uid": 2,
            }
            log_serve_url = dtcloud.tools.config.get('log_serve_url')
            requests.post('%s/api/v1/error_log' % log_serve_url, data=post_data)
        except Exception as e:
            # TODO 错误日志
            print(e)

    @classmethod
    def _operate_log(cls, operation_start_time: datetime, operation_end_time: datetime, uid: str, user: str,
                     param: dict) -> bool:
        """
        操作日志

        :param operation_start_time: 操作开始时间
        :param operation_end_time: 操作结束时间
        :param uid: 操作人员id
        :param user: 操作人员账号
        :param param: 响应值
        :return: T/F
        """
        get_create_operate_log = dtcloud.tools.config.get('get_create_operate_log', False)
        environ = request.httprequest.headers.environ
        request_mode = environ.get('REQUEST_METHOD', '')
        if request_mode == 'GET' and not get_create_operate_log:
            return False
        request_route = environ.get('REQUEST_URI', '')
        request_ip = environ.get('REMOTE_ADDR', '')
        request_params = str(request.params)
        operation_object = request_route.replace('/api/v1', '')
        if request_mode == 'POST' and operation_object == '/upload':
            operation_type = '上传'
        else:
            operation_type = METHOD_TO_OPERATION_TYPE[request_mode]
        threading_1 = threading.Thread(target=cls._request_log_serve, args=(
            operation_object, operation_type, request_mode, uid, user, request_ip, operation_start_time,
            operation_end_time, request_route, request_params, param))
        threading_1.start()
        return True

    @staticmethod
    def _request_log_serve(operation_object: str, operation_type: str, request_mode: str, uid: str, user: str,
                           request_ip: str, operation_start_time: str, operation_end_time: str, request_route: str,
                           request_params: str, param):
        """
        请求log服务生成操作日志

        :param operation_object: 操作对象
        :param operation_type: 操作类型
        :param request_mode: 请求方式
        :param uid: 操作人员id
        :param user: 操作人员账号
        :param request_ip: 请求ip
        :param operation_start_time: 操作开始时间
        :param operation_end_time: 操作结束时间
        :param request_route: 请求路由
        :param request_params: 请求
        :param param: 响应
        """
        try:
            pyload_data = {
                'operation_object': operation_object,
                'operation_type': operation_type,
                'operation_start_time': str(operation_start_time),
                'operation_end_time': str(operation_end_time),
                'operator': ','.join([uid, user]),
                'request_route': request_route,
                'request_mode': request_mode,
                'request_ip': request_ip,
                'request': request_params,
                'response': param,
            }
            post_data = {
                "data": json.dumps(pyload_data),
                "uid": 2,
            }
            log_serve_url = dtcloud.tools.config.get('log_serve_url')
            requests.post('%s/api/v1/operation_log' % log_serve_url, data=post_data)
        except Exception as e:
            # TODO 错误日志
            print(e)
