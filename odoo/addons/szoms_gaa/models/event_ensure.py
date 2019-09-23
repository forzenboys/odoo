from odoo import models,fields,api
from ..zabbix_api.zabbix_client import ZabbixApi


class EventEnsure(models.TransientModel):
    _name = 'zabbix.ensure'

    event_id = fields.Char('事件id')
    message = fields.Char('信息')
    ensure = fields.Boolean('确认问题',default=False)
    close = fields.Boolean('关闭问题',default=False)
    severity = fields.Selection([('0', '未分类'),
                                 ('1', '信息'),
                                 ('2', '警告'),
                                 ('3', '平均'),
                                 ('4', '高'),
                                 ('5', '灾难')], string='更改问题严重性')


    def eventchange(self):
        eventid = self.env.context.get('eventid')
        actions = 0
        for record in self:
            if record.message:
                actions += 2
            if record.close:
                actions += 1
            if record.ensure:
                actions += 4
            if record.severity:
                actions += 8
            print(actions)

