# -*- coding: utf-8 -*-
{
    'name': "zabbix",

    'summary': """
        zabbix集群服务""",

    'description': """
        便捷管理zabbix设备
    """,

    'author': "神州动力数码有限公司",
    'website': "http://www.szpdc.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Network manage',
    'version': '12.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','szoms_monitor'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/zabbix_trigger.xml',
        'views/zabbix_event.xml',
        'views/event_ensure.xml',
        'views/trigger_cron.xml',
        'views/zabbix_alarm.xml',
        'views/trigger_setting.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    # 'post_init_hook': 'add_cron_hook',
}