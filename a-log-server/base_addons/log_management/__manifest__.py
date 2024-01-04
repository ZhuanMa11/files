# -*- coding: utf-8 -*-
{
    'name': "日志管理",
    'summary': '日志管理',
    'category': "dt_log/日志管理",
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
        'security/ir.model.access.csv',
        'views/menuitem.xml',
        'views/login_log.xml',
        'views/operation_log.xml',
        'views/error_log.xml',
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
