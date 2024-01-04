# -*- coding: utf-8 -*-
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# DTcloud Connector 超级API 接口
# QQ:35350428
# 邮件:sale@100china.cn
# 手机：13584935775
# 作者：'Amos'
# 公司网址： www.dtcloud.pw  www.100china.cn www.amoserp.com
# Copyright 昆山一百计算机有限公司 2012-2020 Amos
# 日期：2020/2/13
#  &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

{
    'name': '定时任务',
    'summary': u'定时任务I',
    'category': u'定时任务',
    'sequence': 100,
    'author': 'xcj',
    'website': 'http://www.dtcloud360.com',
    'depends': ['base'],
    'version': '0.1',
    'data': [
        'security/ir.model.access.csv',
        'data/automatically_backing_up_files.xml',
        'views/menuitem.xml',
        'views/backing_up_files_task.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': True,
    'description': """
""",
    'external_dependencies': {
        'python': ['pypeg2', 'requests']
    }
}
