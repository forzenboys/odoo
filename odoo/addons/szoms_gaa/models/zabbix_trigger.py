from odoo import models,fields,api
from ..zabbix_api.zabbix_client import ZabbixApi
import datetime

class ZabbixTrigger(models.Model):
    _name = 'zabbix.trigger'
    _description = 'Zabbix触发器'

    trigger_id = fields.Many2one('zabbix.event','触发器事件')
    eventid = fields.Char(string='事件ID',related='trigger_id.event_id')
    descrtiption = fields.Char('描述信息')
    objectid = fields.Char('对象id')
    host_id = fields.Many2one('zabbix_host',string='触发器主机',ondelete='set null')
    priority = fields.Selection([('0','未分类'),
                                 ('1','信息'),
                                 ('2','警告'),
                                 ('3','平均'),
                                 ('4','高'),
                                 ('5','灾难')],string='优先级',default='0')
    status = fields.Selection([('0','启用'),
                               ('1','禁用')],string='是否启用触发器',default='0')
    last_change = fields.Datetime('最近修改时间')
    state = fields.Selection([('0','待确认'),('1','已确认'),('2','已解决')])


    def get_trigger(self):
        Client = self.env['trigger.settings'].Client()
        trigger = Client.gettrigetID()
        if len(trigger)>0:
            for t in trigger:
                if len(t.get('hosts')) < 1:
                    device = ''
                else:
                    host = t.get('hosts')[0]
                    device = self.env['zabbix_host'].search([('host_id', '=', host.get('hostid'))]).id
                    if not device:
                        self.env['settings_configure'].get_host_data()
                        device = self.env['zabbix_host'].search([('host_id', '=', host.get('hostid'))]).id
                last_time = datetime.datetime.fromtimestamp(int(t["lastchange"]))
                event = self.env['zabbix.event'].check_objects(t.get('triggerid'),Client)
                vals={
                    "objectid" :t.get('triggerid'),
                    "trigger_id" : event,
                    "descrtiption" : t['description'],
                    "priority" : t['priority'],
                    "status" : t['status'],
                    "last_change" : last_time,
                    "host_id" : device,
                    "state":t['state']

                }
                rec = self.env['zabbix.trigger'].search([('objectid', '=', t.get('triggerid'))])
                if rec:
                    self.env['zabbix.trigger'].write(vals)
                else:
                    self.env['zabbix.trigger'].create(vals)
                    self.env['alarm.event'].create_event(vals)


    def event_change(self):
        self.ensure_one()
        action = {
            "type": "ir.actions.act_window",
            "name": "问题更新",
            "res_model": "zabbix.ensure",
            "view_mode": "form"
        }
        action['context']={
            'eventid' :self.eventid
        }
        return action

    def test(self):
        self.get_trigger()