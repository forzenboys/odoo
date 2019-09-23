# -*- coding: utf-8 -*-
{
    'name': "监控系统",

    'summary': """封装增删改接口，独立于基本模块目录，名称：szoms_monitor，host、port、账户密码集成于自有平台设置内""",

    'description': """数据互动""",

    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '12.0.0.1',
    'depends': ['odtree'],

    'data': [
        'security/goups.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/menus.xml',
        'views/templates.xml',
    ],

    'demo': [
        'demo/demo.xml',
    ],
}