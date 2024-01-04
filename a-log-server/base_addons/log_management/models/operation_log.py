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


class OperationLog(models.Model):
    _name = "operation.log"
    _description = "操作日志"
    _order = 'id desc'

    name = fields.Char(string="名称",default="操作日志")
    operation_object = fields.Char(string="操作对象")
    operation_type = fields.Char(string="操作类型")
    request_mode = fields.Char(string="请求方式")
    operator = fields.Char(string="操作人员")
    request_ip = fields.Char(string="请求ip")
    operation_start_time = fields.Char(string="操作开始时间")
    operation_end_time = fields.Char(string="操作结束时间")
    request_route = fields.Char(string="请求路由")
    request = fields.Text(string="请求")
    response = fields.Text(string="响应")
