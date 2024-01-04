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
import os
import threading
import requests
import constants
import dtcloud

SYSTEM_FOLDER_TYPE = "system_file"
PREVIEW_FOLDER_TYPE = "preview_file"
MODEL_FOLDER_TYPE = "model_file"
FILE_CONVERT_URL = dtcloud.tools.config.get('file_convert_url')
RVT_MIDDLE_DIR = dtcloud.tools.config.get('rvt_middle_dir')

LOCK = threading.Lock()


class CommonFileConvert:

    @staticmethod
    def file_convert(file_name: str, ext: str, file_path: str):
        """
        文件转换

        :param file_name: 文件名称
        :param ext: 后缀名
        :param file_path: 文件绝对路径
        """
        # 文件输入文件夹路径
        file_in_dir = file_path.rsplit('\\', 1)[0]
        # 判断需要转换的后缀
        if ext in constants.conversion_ext:
            if ext in constants.model_ext:
                # 文件输出文件夹路径
                file_out_dir = file_in_dir.replace(SYSTEM_FOLDER_TYPE, MODEL_FOLDER_TYPE)
                # 获取中间文件夹路径
                system_dir = file_path.rsplit(SYSTEM_FOLDER_TYPE, 1)[1].rsplit('\\', 1)[0]
                middle_dir = RVT_MIDDLE_DIR + system_dir
                # 调用转换服务
                CommonFileConvert._bim_convert(file_in_dir, file_out_dir, file_name, ext, middle_dir)
            elif ext == 'dwg':
                # TODO 后期根据实际情况修改
                file_dwg_dir = file_in_dir
                file_dxf_dir = file_in_dir.replace(SYSTEM_FOLDER_TYPE, PREVIEW_FOLDER_TYPE)
                CommonFileConvert._dwg_convert(file_dwg_dir, file_dxf_dir)
            else:
                # 输出文件夹路径
                file_out_dir = file_in_dir.replace(SYSTEM_FOLDER_TYPE, PREVIEW_FOLDER_TYPE)
                # 调用转换服务
                CommonFileConvert._document_libre_convert(ext, file_path, file_out_dir)

    @staticmethod
    def _bim_convert(file_in_dir: str, file_out_dir: str, file_name: str, ext: str, middle_dir: str):
        """
        模型转换

        :param file_in_dir: 源文件文件夹路径
        :param file_out_dir: 转换后的文件夹路径
        :param file_name: 文件名称
        :param ext: 文件后缀
        :param middle_dir: 转换中文件夹路径
        """
        try:
            post_data = {
                "file_in_dir": file_in_dir,
                "file_out_dir": file_out_dir,
                "file_name": file_name,
                "file_ext": ext,
                "middle_dir": middle_dir,
            }
            requests.post('%s/web/model/format/convert' % FILE_CONVERT_URL, data=post_data)
        except Exception as e:
            # TODO 日志
            print(e)

    @staticmethod
    def _document_libre_convert(ext: str, file_path: str, file_out_dir: str):
        """
        文件转换(libre_office)

        :param ext: 文件后缀名
        :param file_path: 文件绝对路径
        :param file_out_dir: 转换后的文件夹路径
        """
        try:
            post_data = {
                "ext": ext,
                "file_path": file_path,
                "file_out_dir": file_out_dir,
            }
            requests.post('%s/web/document/libre/convert' % FILE_CONVERT_URL, data=post_data)
        except Exception as e:
            # TODO 日志
            print(e)

    @staticmethod
    def _document_office_convert(file_path: str, file_out_path: str):
        """
        文件转换(office)

        :param file_path: 文件绝对路径
        :param file_out_path: 转换后的文件绝对路径
        """
        try:
            post_data = {
                "file_path": file_path,
                "file_out_path": file_out_path,
            }
            requests.post('%s/web/document/office/convert' % FILE_CONVERT_URL, data=post_data)
        except Exception as e:
            # TODO 日志
            print(e)

    @staticmethod
    def _dwg_convert(file_dwg_dir: str, file_dxf_dir: str):
        """
        图纸转换

        :param file_dwg_dir: dwg文件夹路径
        :param file_dxf_dir: dxf文件夹路径
        """
        try:
            post_data = {
                "file_dwg_dir": file_dwg_dir,
                "file_dxf_dir": file_dxf_dir,
            }
            requests.post('%s/web/dwg/convert' % FILE_CONVERT_URL, data=post_data)
        except Exception as e:
            # TODO 日志
            print(e)
