# -*- coding: utf-8 -*-
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# DTCloud v2.0
# QQ: 190066183
# 邮件: 190066183@qq.com
# 手机: 18118160329
# 作者: 'zyf_KyoRyu'
# 公司网址: http://www.dtcloud360.com
# Copyright 中亿丰数字科技有限公司 2012-2022 KyoRyu
# 日期: 2022/10/20
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
import json
import subprocess
import threading
import dtcloud

from dtcloud import http
from utils.log.logger import output_log
from dtcloud.addons.web.controllers.main import Home
from .model_format_convert import ModelFormatConvert


class DwgConvert(Home):

    @http.route('/web/dwg/convert', type='http', auth="none", csrf=False, method=["POST"], website=True, cors="*")
    def dwg_to_dxf(self, **kw):
        """
        图纸转换\n
        :param kw: dwg文件输入路径，dxf文件输出路径
        :return: 转换结果
        """
        DwgConvert._dwg_convert(kw)
        return json.dumps({'code': 0, 'message': '返回成功'})

    @staticmethod
    def _dwg_convert(kw):
        """
        dwg转换\n
        :param kw: dwg文件夹路径 dxf文件夹路径
        :return: 文件转换
        """
        try:
            # dwg文件输入路径
            file_dwg_dir = kw.get('file_dwg_dir', '')
            # dxf文件输出路径
            file_dxf_dir = kw.get('file_dxf_dir', '')
            t1 = threading.Thread(target=DwgConvert._dwg_to_dxf, args=(file_dwg_dir, file_dxf_dir))
            t1.start()
            return True
        except Exception as e:
            output_log(str(e), "_dwg_convert", kw, "dwg")
            data = {
                "code": -1,
                "message": '转换失败!',
            }
            return json.dumps(data)

    @staticmethod
    def _dwg_to_dxf(file_dwg_dir: str, file_dxf_dir: str):
        """
        调用exe转换\n
        :param file_dwg_dir: dwg文件夹路径
        :param file_dxf_dir: dxf文件夹路径
        :return: 文件转换
        """
        data = {
            'file_in_dir': file_dwg_dir,
            'file_out_dir': file_dxf_dir,
            'conversion_type': '图纸转换',
        }
        try:
            # PARAMS:
            # Input folder
            # Output folder
            # Output version: ACAD9, ACAD10, ACAD12, ACAD14, ACAD2000, ACAD2004, ACAD2007, ACAD20010, ACAD2013, ACAD2018
            # Output file type: DWG, DXF, DXB
            # Recurse Input Folder: 0, 1
            # Audit each file: 0, 1
            # (Optional) Input files filter: *.DWG, *.DXF
            dwg2dxf_exe_path = dtcloud.tools.config.get('dwg2dxf_exe_path')
            TEIGHA_PATH = dwg2dxf_exe_path
            INPUT_FOLDER = file_dwg_dir
            OUTPUT_FOLDER = file_dxf_dir
            OUTVER = "ACAD2018"
            OUTFORMAT = "DXF"
            RECURSIVE = "0"
            AUDIT = "1"
            INPUTFILTER = "*.DWG"
            # Command to run
            cmd = [TEIGHA_PATH, INPUT_FOLDER, OUTPUT_FOLDER, OUTVER, OUTFORMAT, RECURSIVE, AUDIT, INPUTFILTER]
            subprocess.run(cmd, shell=True)
            data['result'] = '成功'
            data['message'] = f'转换成功，地址--{file_dxf_dir}'
            ModelFormatConvert.create_conversion_record(data)
        except Exception as e:
            data['result'] = '失败'
            data['message'] = f'转换失败,{e}'
            ModelFormatConvert.create_conversion_record(data)
