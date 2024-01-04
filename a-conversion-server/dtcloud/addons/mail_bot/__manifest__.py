# -*- coding: utf-8 -*-
# Part of DTCloud. See LICENSE file for full copyright and licensing details.

{
    'name': 'DTCloudBot',
    'version': '1.2',
    'category': '工具/机器人',
    'summary': 'Add DTCloudBot in discussions',
    'description': "",
    'website': 'https://www.dtcloud360.com/page/discuss',
    'depends': ['mail'],
    'auto_install': True,
    'installable': True,
    'application': False,
    'data': [
        'views/assets.xml',
        'views/res_users_views.xml',
        'data/mailbot_data.xml',
    ],
    'demo': [
        'data/mailbot_demo.xml',
    ],
    'qweb': [
        'static/src/bugfix/bugfix.xml',
    ],
    'license': 'LGPL-3',
}
