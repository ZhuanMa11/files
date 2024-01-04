# -*- coding: utf-8 -*-
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# AmosERP dtcloud11.0
# QQ:35350428
# 邮件:35350428@qq.com
# 手机：13584935775
# 作者：'amos'
# 公司网址： www.dtcloud.pw  www.100china.cn www.amoserp.com
# Copyright 昆山一百计算机有限公司 2012-2018 Amos
# 日期：2020/2/16
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

from dtcloud import api, fields, models, tools, SUPERUSER_ID, _


class hr_department(models.Model):
    _name = "hr.department"
    _description = '部门'

    name = fields.Char(u'部门名称', required=True)

    sequence = fields.Integer(default=10)
    child_id = fields.One2many('hr.department', 'parent_id', string='下级部门')
    parent_id = fields.Many2one('hr.department', string='上级部门', index=True, ondelete="restrict")

    company_id = fields.Many2one('res.company', string='公司', required=True,
                                 default=lambda self: self.env.company.id, context={'user_preference': True})
    active = fields.Boolean(default=True)
