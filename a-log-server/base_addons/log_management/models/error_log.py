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
from dtcloud import fields, models


class ErrorLog(models.Model):
    _name = "error.log"
    _description = "错误日志"
    _order = 'id desc'

    name = fields.Char(string="错误日志",default="错误日志")
    request_route = fields.Char(string="请求路由")
    request_mode = fields.Char(string="请求方式")
    operation_type = fields.Char(string="操作类型")
    operation_object = fields.Char(string="操作对象")
    operator = fields.Char(string="操作人员")
    error_function = fields.Char(string="错误方法")
    error_path = fields.Char(string="错误路径")
    error_details = fields.Text(string="错误详情")
    request = fields.Text(string="请求")

