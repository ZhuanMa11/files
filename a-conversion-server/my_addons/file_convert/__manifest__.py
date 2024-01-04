# -*- coding: utf-8 -*-
{
    'name': "文件转换服务",
    'summary': '文件转换服务',
    'version': '1.0',
    'category': "文件转换服务",
    'sequence': 80,
    'author': 'ZYF-XCJ',
    'website': '',
    'depends': [],
    'data': [
        'security/ir.model.access.csv',
        'views/conversion_record.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': True,
    'description': """

""",
    'external_dependencies': {
        # 'python': ['pypeg2', 'requests', "jsonpath"]
    }
}
