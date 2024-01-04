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
import base64
import os
import shutil
import threading
import time
import urllib
import zipfile
from shutil import copyfile

import constants
import dtcloud
from base_addons.common.api_parse_sdb.parse_sdb import ParseSdb
from dtcloud.http import request, content_disposition
from base_addons.common.api_crud.api_create import CommonApiCreate
from base_addons.common.api_file.api_file_convert import CommonFileConvert
from base_addons.common.api_file.file_path import CommonFilePath

PREVIEW_FOLDER_TYPE = "preview_file"
MODEL_FOLDER_TYPE = "model_file"

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


class FileApiService:

    @classmethod
    def upload_file(cls, kw: dict):
        """
        上传文件主函数

        :param kw: 接口入参
        :return: 数据和消息key
        """
        pool = request.env
        name = kw.get('name')  # 获取上传文件的文件名
        ext = kw.get('ext')  # 获取上传文件的后缀名
        model = kw.get('model')  # 获取上传文件的模块名
        md5 = kw.get('md5')  # 获取文件的唯一标识符
        size = kw.get('size')  # 获取文件的唯一标识符
        base_dir = CommonFilePath.get_file_save_dir("system_file")
        dt = model.replace('.', '_') if model else "others"
        file_dir = os.path.join(base_dir, str(dt))
        if request.httprequest.files:
            upload_file = request.params["files"]
            # 创建文件记录
            data = {'name': name, 'ext': ext, 'md5': md5, 'size': size}
            file_library = CommonApiCreate.create_single_record(pool, model, '2', data)
            # 拼接文件保存绝对路径
            file_path = os.path.join(file_dir, str(file_library.id))
            file_path = os.path.join(file_path, md5)
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            file_path = os.path.join(file_path, name + '.' + ext)
            # 获取文件保存相对路径
            path = 'system_file/static' + file_path.split('\system_file\static')[1].replace('\\', '/')
            file_library.path = path
            # 获取文件下载地址
            download_list = list(CommonFilePath.get_file_download_path(file_library._name, file_library.id))
            file_library.download_path = download_list
            # 生成对应的view_path
            view_path = CommonFilePath.get_file_preview_path(path, ext)
            file_library.view_path = view_path
            # 多线程调用文件保存和转换服务函数
            threading.Thread(target=cls._file_save_and_convert, args=(name, ext, file_path, upload_file)).start()
            # 返回前端文件信息
            data = {
                "file_id": file_library.id,
                "file_name": file_library.name,
                "file_ext": file_library.ext,
                "file_full_name": file_library.name + '.' + file_library.ext,
                "view_path": view_path,
                "download_list": download_list,
            }
            if ext in constants.model_ext:
                data['sdb_path'] = view_path.replace(view_path.rsplit('.', 1)[-1], 'sdb')
            return data, 5
        return {}, 6

    @classmethod
    def _file_save_and_convert(cls, file_name: str, ext: str, file_path: str, upload_file):
        """
        文件存储和转换

        :param file_name: 文件名称
        :param ext: 文件后缀
        :param file_path: 文件绝对路径
        :param upload_file: 文件流
        """
        cls._upload_file(file_path, upload_file)
        CommonFileConvert.file_convert(file_name, ext, file_path)

    @staticmethod
    def _upload_file(file_path: str, upload_file):
        """
        保存文件流

        :param file_path: 文件路径(包含文件名)
        :param upload_file: 文件流
        """
        file_dir = file_path.rsplit("\\", 1)[0]
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        upload_file.save(file_path)

    @staticmethod
    def download_file(kw: dict):
        """
        下载指定文件

        :param kw: 接口入参
        :return: 下载流
        """
        model = kw.get('model')
        res_id = kw.get('res_id')
        obj = request.env['%s' % model].sudo().browse(res_id)
        filename = obj.name + '.' + obj.ext
        addons = dtcloud.tools.config.get('addons_path').split(',')[-1]
        headers = [('X-Content-Type-Options', 'nosniff')]
        file_path = addons + '/' + obj.path
        with open(file_path, 'rb') as f:
            content_base64 = base64.b64encode(f.read())
            content_base64 = base64.b64decode(content_base64)
        headers.append(('Content-Length', len(content_base64)))
        headers.append(('charset', 'utf-8'))
        headers.append(('Content-Disposition', content_disposition(filename)))
        response = request.make_response(content_base64, headers)
        return response

    @staticmethod
    def stream_download_file(kw: dict):
        """
        流式下载指定文件

        :param kw: 接口入参
        :return: 下载流
        """
        model = kw.get('model')
        res_id = kw.get('res_id')
        obj = request.env['%s' % model].sudo().browse(res_id)
        filename = obj.name + '.' + obj.ext
        addons = dtcloud.tools.config.get('addons_path').split(',')[-1]
        headers = [('Content-Type', 'application/octet-stream'), ('X-Content-Type-Options', 'nosniff')]
        file_path = addons + '/' + obj.path

        def content_stream():
            with open(file_path, 'rb') as f:
                while True:
                    data = f.read(20 * 1024 * 1024)
                    if not data:
                        break
                    yield data

        headers.append(('Content-Length', os.path.getsize(file_path)))
        headers.append(('charset', 'utf-8'))
        headers.append(('Content-Disposition', content_disposition(filename)))
        response = request.make_response(content_stream(), headers)
        return response

    @staticmethod
    def check_preview_file(kw: dict) -> int:
        """
        检查文件是否可以预览

        :param kw: 接口入参
        :return: code编码 7/8 7:可以 8:不可以
        """
        pool = request.env
        model = kw.get('model')
        res_id = kw.get('res_id')
        record = pool[model].sudo().search([('id', '=', int(res_id))])
        if not record:
            return 8
        if record.ext in constants.preview_ext:
            addons_path = dtcloud.tools.config.get('addons_path').split(',')[-1]
            if record.ext in constants.model_ext:
                path = urllib.parse.unquote(record.view_path).split(MODEL_FOLDER_TYPE, 1)[-1]
                view_path = addons_path + '/' + MODEL_FOLDER_TYPE + path
                sdb_path = view_path.replace(view_path.rsplit('.', 1)[-1], 'sdb')
                if os.path.exists(view_path) and os.path.exists(sdb_path):
                    return 9
            else:
                path = urllib.parse.unquote(record.view_path).split(PREVIEW_FOLDER_TYPE, 1)[-1]
                view_path = addons_path + '/' + PREVIEW_FOLDER_TYPE + path
                if os.path.exists(view_path):
                    return 9
        return 10

    @classmethod
    def get_file_path_by_file_id(cls, file_id: int):
        """
        根据file_id获取文件保存路径

        :param file_id: 文件id
        :return: 文件绝对路径
        """
        pool = request.env
        record = pool['file.library'].sudo().browse(int(file_id))
        addons_path = dtcloud.tools.config.get('addons_path').split(',')[-1]
        file_path = addons_path + '/' + record.path
        return file_path, record.name, record.ext

    @classmethod
    def create_folder(cls, data_list, path):
        """
        创建需要打包下载的文件目录及copy文件

        :param data_list: 需要创建文件夹的列表
        :param path: 当前所在的地址
        """
        for res in data_list:
            if res['category'] == 'drawing':
                file_path, name, ext = cls.get_file_path_by_file_id(int(res['file_id']))
                target_path = path + "/" + name + '.' + ext
                copyfile(file_path, target_path)
            elif res['category'] == 'document':
                path = path + "/" + res['name']
                if not os.path.exists(path):
                    os.makedirs(path)
                if 'children' in res:
                    data_list = res['children']
                    cls.create_folder(data_list, path)
                path = path.replace('/', '\\')
                path = path.rsplit('\\', 1)[0]

    @staticmethod
    def zip(dirname, zipfile_name):
        """
        将目标文件夹打包压缩

        :param dirname: 需要压缩的文件夹
        :param zipfile_name: 压缩后的文件全路径
        :return:
        """
        filelist = []
        if os.path.isfile(dirname):
            filelist.append(dirname)
        else:
            for root, dirs, files in os.walk(dirname, topdown=False):
                if not files and not dirs:
                    filelist.append(root)
                for name in files:
                    filelist.append(os.path.join(root, name))
        zf = zipfile.ZipFile(zipfile_name, "w", zipfile.ZIP_DEFLATED)
        for tar in filelist:
            arcname = tar[len(dirname):]
            zf.write(tar, arcname)
        zf.close()
        return ''

    @staticmethod
    def delete_copy_folder(delete_path):
        """
        删除copy过来的文件

        :param delete_path:
        :return:
        """
        if os.path.exists(delete_path):
            shutil.rmtree(delete_path)

    @classmethod
    def batch_download_file(cls, kw):
        """
        批量下载

        :param kw:  接口入参
        :return: 下载地址，状态码id，接口信息
        """
        data_list = kw.get('data_list', '')
        if data_list == '[]' or not data_list:
            return {}, 6, '-未选择文件或文件夹'
        data_list = eval(data_list)
        data_time = time.time()
        data_time = str(data_time).replace('.', '')
        base_dir = BASE_DIR + f"/static/download_zip/{data_time}"
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
        cls.create_folder(data_list, path=base_dir)
        cls.zip(base_dir, base_dir + '.zip')
        cls.delete_copy_folder(base_dir)
        server_url = dtcloud.tools.config.get('server_url')
        download_path = server_url + f'/file_api/static/download_zip/{data_time}.zip'
        return {"download_path": download_path}, 5, ''

    @classmethod
    def get_file_info_by_file_id(cls, file_id: int):
        """
        根据file_id获取文件保存路径

        :param file_id: 文件id
        :return: 文件绝对路径
        """
        pool = request.env
        record = pool['file.library'].sudo().browse(int(file_id))
        return record

    @staticmethod
    def get_sdb_path_by_record(record) -> str:
        """
        根据文件记录获取sdb文件地址

        :param record: 文件记录
        :return: sdb_path
        """
        addons_path = dtcloud.tools.config.get('addons_path').split(',')[-1]
        view_path = MODEL_FOLDER_TYPE + record.view_path.rsplit(MODEL_FOLDER_TYPE)[-1]
        sdb_path = addons_path + '/' + view_path.replace(view_path.rsplit('.', 1)[-1], 'sdb')
        sdb_path = urllib.parse.unquote(sdb_path)
        return sdb_path

    @classmethod
    def get_model_tree(cls, file_id: int) -> tuple:
        """
        根据文件id获取模型tree

        :param file_id:
        :return:
        """
        record = cls.get_file_info_by_file_id(int(file_id))
        sdb_path = cls.get_sdb_path_by_record(record)
        try:
            data_tree_list = [ParseSdb.parse_sdb_get_model_tree(urllib.parse.unquote(sdb_path))]
        except Exception as e:
            data_tree_list = list()
        return record, data_tree_list

    @classmethod
    def parse_model(cls, kw):
        """
        解析模型

        :param kw: 接口入参
        :return: 构建信息，状态码id，接口信息
        """
        data = kw.get('data')
        if data == '[]' or not data:
            return [], 6, '-没有可解析的模型'
        data = eval(data)
        for data_dict in data:
            for model in data_dict['model_list']:
                for file_id in model['model_ids']:
                    record = cls.get_file_info_by_file_id(int(file_id))
                    value = {
                        'file_id': record.id,
                        'name': record.name,
                        'ext': record.ext,
                        'full_name': f"{record.name}.{record.ext}",
                        'view_path': record.view_path,
                    }
                    if 'model_list' not in model:
                        model['model_list'] = []
                    model['model_list'].append(value)
                model.pop('model_ids')
        return data, 5, ''

    @classmethod
    def get_build_properties(cls, kw):
        """
        获取构建属性

        :param kw: 接口入参
        :return: 构建属性，状态码id
        """
        guid = kw.get('guid')
        file_id = kw.get('file_id')
        record = cls.get_file_info_by_file_id(int(file_id))
        sdb_path = cls.get_sdb_path_by_record(record)
        try:
            data_list = ParseSdb.parse_sdb_get_build_properties(guid, sdb_path)
        except Exception as e:
            data_list = list()
        return data_list, 5

    @classmethod
    def get_pc_build_properties(cls, kw):
        """
        获取pc构建

        :param kw: 接口入参
        :return:
        """
        file_ids = kw.get('file_ids')
        where_data = kw.get('where_data')
        if file_ids == '[]' or not file_ids:
            return {}, 6, '未勾选模型'
        file_ids = eval(file_ids)
        return_data_list = list()
        for file_id in file_ids:
            record = cls.get_file_info_by_file_id(int(file_id))
            sdb_path = cls.get_sdb_path_by_record(record)
            try:
                data_list = ParseSdb.parse_sdb_get_all_pc_build_properties(where_data, sdb_path, file_id)
            except Exception as e:
                data_list = list()
            return_data_list += data_list
        return return_data_list, 5
