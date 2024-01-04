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
import urllib

import constants
import dtcloud

ADDONS_PATH = dtcloud.tools.config.get('addons_path').split(',')[-1]
SYSTEM_FOLDER_TYPE = "system_file"
PREVIEW_FOLDER_TYPE = "preview_file"
MODEL_FOLDER_TYPE = "model_file"
SERVER_URL = dtcloud.tools.config.get('server_url')


class CommonFilePath:

    @staticmethod
    def get_file_save_dir(folder_type: str) -> str:
        """
        获取文件的存放文件夹路径

        :param folder_type: 文件类型
        :return: 文件夹路径
        """
        base_dir = ADDONS_PATH + r'\{0}\static'.format(folder_type)
        return base_dir

    @staticmethod
    def get_file_preview_path(path: str, ext: str) -> str:
        """
        获取文件的预览地址

        :param path: 源文件相对路径
        :param ext: 源文件后缀名
        :return: 预览地址
        """
        if ext in constants.preview_ext:
            if ext == 'dwg':
                preview_path = CommonFilePath._dwg_preview_path(path)
            elif ext in constants.model_ext:
                preview_path = CommonFilePath._bim_preview_path(path, ext)
            else:
                preview_path = CommonFilePath._document_preview_path(path, ext)
            preview_path = '%s/%s' % (SERVER_URL, preview_path)
            preview_path = urllib.request.quote(preview_path, safe='/:?=&', encoding='utf-8')
        else:
            preview_path = ''
        return preview_path

    @staticmethod
    def _dwg_preview_path(path: str) -> str:
        """
        生成dwg的预览地址

        :param path: 源文件地址
        :return: dwg预览地址
        """
        dwg_preview = path.replace(SYSTEM_FOLDER_TYPE, PREVIEW_FOLDER_TYPE)
        dwg_preview_path = dwg_preview.replace(path.rsplit('.', 1)[-1], 'dxf')
        return dwg_preview_path

    @staticmethod
    def _document_preview_path(path: str, ext: str) -> str:
        """
        文件预览相对路径

        :param path: 源文件相对路径
        :param ext: 源文件后缀名
        :return: 预览相对路径
        """
        if ext in constants.conversion_ext:
            document_preview_path = path.replace(SYSTEM_FOLDER_TYPE, PREVIEW_FOLDER_TYPE)
            convert_ext = "pdf" if ext not in ('xls', 'xlsx') else "html"
            document_preview_path = document_preview_path.replace(path.rsplit('.', 1)[-1], convert_ext)
        else:
            document_preview_path = path
        return document_preview_path

    @staticmethod
    def _bim_preview_path(path: str, ext: str) -> str:
        """
        模型文件预览相对路径

        :param path: 源文件相对路径
        :param ext: 源文件后缀名
        :return: 预览相对路径
        """
        bim_preview_path = path.replace(SYSTEM_FOLDER_TYPE, MODEL_FOLDER_TYPE)
        bim_preview_path = bim_preview_path.replace(path.rsplit('.', 1)[-1], "zip")
        return bim_preview_path

    @staticmethod
    def get_file_download_path(res_model: str, res_id: str) -> tuple:
        """
        获取文件下载路径

        :param res_model: 文件model
        :param res_id: 文件ID
        :return: 下载地址
        """
        download = '%s/api/v1/download/%s' % (SERVER_URL, res_id)
        stream_download = '%s/api/v1/stream_download/%s' % (SERVER_URL, res_id)
        download = urllib.request.quote(download, safe='/:?=&', encoding='utf-8')
        stream_download = urllib.request.quote(stream_download, safe='/:?=&', encoding='utf-8')
        return download, stream_download
