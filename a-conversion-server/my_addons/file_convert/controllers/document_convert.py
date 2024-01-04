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
import pythoncom
import dtcloud

from dtcloud import http
from win32com import client
from utils.log.logger import output_log
from dtcloud.addons.web.controllers.main import Home
from .model_format_convert import ModelFormatConvert

LOCK = threading.Lock()
OFFICE_EXE = dtcloud.tools.config.get('libre_office_path')


class DocumentConvert(Home):

    @http.route('/web/document/libre/convert', type='http', auth="none", csrf=False, method=["POST"], website=True,
                cors="*")
    def document_convert(self, **kw: dict):
        """
        文件转换为预览文件\n
        :param kw: 原文件路径 输出路径 源文件后缀
        :return: 转换后文件
        """
        DocumentConvert._document_convert(kw)
        return json.dumps({'code': 0, 'message': '返回成功'})

    @staticmethod
    def _document_convert(kw: dict):
        """
        文件转换为预览文件\n
        :param kw: 原文件路径 输出路径 源文件后缀
        :return: 转换后文件
        """
        try:
            ext = kw.get('ext', '')
            file_path = kw.get('file_path', '')
            file_out_dir = kw.get('file_out_dir', '')
            convert_ext = "pdf" if ext not in ('xls', 'xlsx') else "html"
            t = threading.Thread(target=DocumentConvert._libre_office_convert,
                                 args=(convert_ext, file_path, file_out_dir))
            t.start()
            return True
        except Exception as e:
            output_log(str(e), "_document_convert", kw, "document_libre")
            data = {
                "code": -1,
                "message": '转换失败!',
            }
            return json.dumps(data)

    @staticmethod
    def _libre_office_convert(convert_type: str, file_path: str, file_out_dir: str):
        """
        文件转换exe执行
        :param convert_type: 转换后后缀
        :param file_path: 源文件路径
        :param file_out_dir: 转换后文件夹
        :return: 转换后的文件
        """
        file_name, file_ext = file_path.replace('\\', '/').rsplit('/', 1)[-1].rsplit('.', 1)
        data = {
            'file_name': file_name,
            'file_ext': file_ext,
            'file_in_dir': file_path,
            'file_out_dir': file_out_dir,
            'conversion_type': '文档转换',
        }
        try:
            LOCK.acquire()
            # os.system('"%s" --headless --convert-to "%s" "%s"  --outdir "%s"' % (OFFICE_EXE, convert_type, file_path, file_out_dir))
            cmd= '"%s" --headless --convert-to "%s" "%s"  --outdir "%s"' % (OFFICE_EXE, convert_type, file_path, file_out_dir)
            subprocess.run(cmd, shell=True)
            LOCK.release()
            data['result'] = '成功'
            data['message'] = f'转换成功，地址--{file_out_dir}'
            ModelFormatConvert.create_conversion_record(data)
        except Exception as e:
            data['result'] = '失败'
            data['message'] = f'转换失败,{e}'
            ModelFormatConvert.create_conversion_record(data)


    @http.route('/web/document/office/convert', type='http', auth="none", csrf=False, method=["POST"], website=True,
                cors="*")
    def word_office_convert(self, **kw: dict):
        """
        特殊word转换（由于审查文档图片问题，需要office转换，服务器需要装office）\n
        :param kw: 文件输入全路径 文件输出全路径
        :return: 执行结果
        """
        file_path = kw.get('file_path', '')
        file_out_path = kw.get('file_out_path', '')
        t = threading.Thread(target=DocumentConvert._wold_convert,
                             args=(file_path, file_out_path, kw))
        t.start()
        return json.dumps({'code': 0, 'message': '返回成功'})

    @staticmethod
    def _wold_convert(file_path: str, file_out_path: str, kw: dict):
        """
        office.exe word转换
        :param file_path: 文件输入全路径
        :param file_out_path: 文件输出全路径
        :param kw: url请求参数
        :return: 转换结果
        """
        file_name, file_ext = file_path.replace('\\', '/').rsplit('/', 1)[-1].rsplit('.', 1)
        data = {
            'file_name': file_name,
            'file_ext': file_ext,
            'file_in_dir': file_path,
            'file_out_dir': file_out_path,
            'conversion_type': '文档转换',
        }
        try:
            pythoncom.CoInitialize()
            wordhandle = client.Dispatch("Word.Application")
            wordhandle.Visible = 0  # 后台运行，不显示
            wordhandle.DisplayAlerts = 0  # 不警告
            doc = wordhandle.Documents.Open(file_path)
            doc.SaveAs(file_out_path, 17)  # txt=4, html=10, docx=16， pdf=17
            doc.Close()
            wordhandle.Quit()
            data['result'] = '成功'
            data['message'] = f'转换成功，地址--{file_out_path}'
            ModelFormatConvert.create_conversion_record(data)
            return True
        except Exception as e:
            data['result'] = '失败'
            data['message'] = f'转换失败,{e}'
            ModelFormatConvert.create_conversion_record(data)

            return False

