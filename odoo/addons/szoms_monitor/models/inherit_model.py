# -*- coding: utf-8 -*-
from odoo import models, fields, api


class inheritResGroups(models.Model):
    _inherit = 'res.groups'


class inheritIrRule(models.Model):
    _inherit = 'ir.rule'


class inheritIrModelAccesse(models.Model):
    _inherit = 'ir.model.access'


class inheritIrResCategory(models.Model):
    _inherit = 'ir.module.category'


class inheritIrUiView(models.Model):
    _inherit = 'ir.ui.view'


class inheritResPartner(models.Model):
    _inherit = 'res.partner'


class inheritCompany(models.Model):
    _inherit = 'res.company'

class inheritResUsers(models.Model):
    _inherit = 'res.users'
