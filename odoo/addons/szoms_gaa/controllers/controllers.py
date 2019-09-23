# -*- coding: utf-8 -*-
from odoo import http

# class Zabbix(http.Controller):
#     @http.route('/zabbix/zabbix/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/zabbix/zabbix/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('zabbix.listing', {
#             'root': '/zabbix/zabbix',
#             'objects': http.request.env['zabbix.zabbix'].search([]),
#         })

#     @http.route('/zabbix/zabbix/objects/<model("zabbix.zabbix"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('zabbix.object', {
#             'object': obj
#         })