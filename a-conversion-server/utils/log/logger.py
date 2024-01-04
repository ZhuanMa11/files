# -*- coding: utf-8 -*-
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# DTCloud v2.0
# QQ: 190066183
# 邮件: 190066183@qq.com
# 手机: 18118160329
# 作者: 'zyf_KyoRyu'
# 公司网址: http://www.dtcloud360.com
# Copyright 中亿丰数字科技有限公司 2012-2022 KyoRyu
# 日期: 2022/10/8
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
import datetime
import logging
import os

# 创建日志器对象
import dtcloud

LOGGER = logging.getLogger(__name__)
# 设置logger可输出日志级别范围
LOGGER.setLevel(logging.INFO)
# 设置格式并赋予handler
FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# 不同转换不同的错误日志
# 模型转换
LOG_FILE_RVT = dtcloud.tools.config.get('log_file_rvt')
# 图纸转换
LOG_FILE_DWG = dtcloud.tools.config.get('log_file_dwg')
# libre文件转换
LOG_FILE_DOCUMENT_LIBRE = dtcloud.tools.config.get('log_file_document_libre')
# office文件转换
LOG_FILE_DOCUMENT_OFFICE = dtcloud.tools.config.get('log_file_document_office')


def output_log(message, method, kw, convert_type="document_office"):
    """
    日志输出\n
    :param message: 错误信息
    :param method: 错误方法名
    :param kw: 参数
    :param convert_type: 转换服务类型
    :return: 输出日志
    """
    # 添加日志文件handler，用于输出日志到文件中
    if convert_type == "rvt":
        log_file_path = LOG_FILE_RVT
    elif convert_type == "dwg":
        log_file_path = LOG_FILE_DWG
    elif convert_type == "document_libre":
        log_file_path = LOG_FILE_DOCUMENT_LIBRE
    else:
        log_file_path = LOG_FILE_DOCUMENT_OFFICE
    log_name = datetime.datetime.now().strftime('%Y-%m-%d')
    log_file_name = os.path.join(log_file_path, log_name)
    file_handler = logging.FileHandler(filename=log_file_name, encoding='UTF-8')
    LOGGER.addHandler(file_handler)
    file_handler.setFormatter(FORMATTER)
    LOGGER.info("=======================错误日志开始===========================")
    LOGGER.info("调用方法：%s", method)
    LOGGER.info("参数：%s", kw)
    LOGGER.error(message, exc_info=True)
    LOGGER.info("=======================错误日志结束===========================")
    LOGGER.removeHandler(file_handler)
