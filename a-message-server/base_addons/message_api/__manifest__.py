# -*- coding: utf-8 -*-
{
    'name': "接口返回消息状态码管理",
    'summary': '接口消息状态码管理',
    'category': "dt_base/消息状态码管理",
    'author': "zyf_xcj",
    'website': "http://www.dtcloud360.com",
    'depends': [],
    'version': '1.0',  # 版本号注意, 两位，初始版本为1.0
    'installable': True,
    'application': True,
    'auto_install': True,
    'license': 'LGPL-3',
    'price': '100',  #  Odoo Apps Store上显示的时候以美元显示
    'currency': 'USD',  # 全部以美元为单位
    'data': [
        'data/message.xml',
        'security/ir.model.access.csv',
        'views/message_management.xml',
    ],
    'images': [
    ],
    'assets': {
        'web.assets_backend': [
        ],
        'web.assets_qweb': [
        ],
    },
    'description': """""",  # 建议为空
}
