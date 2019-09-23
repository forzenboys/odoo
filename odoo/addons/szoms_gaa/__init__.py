# -*- coding: utf-8 -*-

from . import controllers
from . import models
from . import zabbix_api
from odoo import api, fields, SUPERUSER_ID

# def add_cron_hook(cr,registry):
#     env = api.Environment(cr, SUPERUSER_ID, {})
#     trigger_cron = {'name': 'Book 1', 'date_release': fields.Date.today()}
#     env['zabbix.trigger'].create(trigger_cron)