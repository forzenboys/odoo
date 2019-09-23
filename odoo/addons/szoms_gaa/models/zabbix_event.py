from odoo import models,fields,api
from ..zabbix_api.zabbix_client import ZabbixApi
from ..zabbix_api.client import ZabbixClient
import datetime

class ZabbixProblem(models.Model):
    _name = 'zabbix.event'
    _description = 'zabbix 事件'

    event_id = fields.Char('事件id')
    source = fields.Selection([('0','触发器创建的事件'),
                               ('1','发现规则创建事件'),
                               ('2','活动代理自动创建的事件'),
                               ('3','内部事件')],
                                    string='事件来源',
                                    default='0')
    object = fields.Selection([('0','触发器'),
                               ('1','已发现的主机'),
                               ('2','已发现的服务'),
                               ('3','自动注册的主机'),
                               ('4','item'),
                               ('5','LLD规则')],
                                string='事件对象',
                                default='0')
    severity = fields.Selection([('0', '未分类'),
                                 ('1', '信息'),
                                 ('2', '警告'),
                                 ('3', '平均'),
                                 ('4', '高'),
                                 ('5', '灾难')], string='严重程度')
    objectid = fields.Char('事件对象id')
    name = fields.Char('事件描述')
    device = fields.Many2one('zabbix_host','事件主机')
    clock = fields.Datetime('告警时间')
    ns = fields.Char('纳秒')
    acknowledged = fields.Selection([('0','未确认'),
                                     ('1','已确认')],
                                    string='问题确认',
                                    default='0')
    r_event = fields.Char('完成事件id')
    userid = fields.Char('手动关闭事件的用户')
    suppressed = fields.Selection([('0','正常'),('1','抑制')],string='事件抑制状态',default='0')


    def sync(self):
        # url, user, pwd = self.env['settings_configure'].get_config()
        # print(url, user, pwd)
        # events = ZabbixApi.event_get(url, user, pwd)
        Client = self.env['trigger.settings'].Client()
        events = Client.event_get()
        print(events)
        for p in events:
            time_c = int(p.get('clock'))
            clock = datetime.datetime.fromtimestamp(time_c)
            # time_ns = int(p.get('ns'))
            # ns = datetime.datetime.fromtimestamp(time_ns)
            if len(p.get('hosts'))<1:
                device = ''
            else:
                host =p.get('hosts')[0]
                device = self.env['zabbix_host'].search([('host_id', '=', host.get('hostid'))]).id
                if not device:
                    self.env['settings_configure'].get_host_data()
                    device = self.env['zabbix_host'].search([('host_id', '=', host.get('hostid'))]).id

            vals = {
                "event_id" : p.get('eventid'),
                "clock" :clock,
                "source":p.get('source'),
                "object":p.get('object'),
                "severity":p.get('severity'),
                "objectid":p.get('objectid'),
                "ns":p.get('ns'),
                "device":device,
                "name" : p.get('name'),
                "acknowledged" : p.get('acknowledged'),
                "r_event":p.get('r_eventid'),
                "userid":p.get("userid"),
                "suppressed":p.get("suppressed")
            }
            print(vals)
            rec = self.env['zabbix.event'].search([('event_id', '=', p.get('eventid'))])
            if rec:
                self.env['zabbix.event'].write(vals)
            else:
                self.env['zabbix.event'].create(vals)


    def check_objects(self,objectid,Client):
        if objectid == "0":
            return ''

        record = Client.triggergetevents(objectid)[0]
        # url, user, pwd = self.env['settings_configure'].get_config()
        # print(url, user, pwd)
        # record = ZabbixApi.triggergetevents(url, user, pwd,objectid)[0]
        rec = self.env['zabbix.event'].search([('objectid', '=', objectid),
                                               ('r_event','=','0'),
                                               ('severity','!=',"0")])
        if record.get('eventid') != rec.event_id:
            self.createvals(record)
        if rec:
            return rec.id
        else:
            rec = ZabbixApi.triggergetevents(url, user, pwd,objectid)
            if len(rec)<1:
                return ''
            event = rec[0]
            self.createvals(event)

    def createvals(self,event):
        time_c = int(event.get('clock'))
        clock = datetime.datetime.fromtimestamp(time_c)
        if len(event.get('hosts')) < 1:
            device = ''
        else:
            host = event.get('hosts')[0]
            device = self.env['zabbix_host'].search([('host_id', '=', host.get('hostid'))]).id
            if not device:
                self.env['zabbix.category'].sysn()
                device = self.env['zabbix_host'].search([('host_id', '=', host.get('hostid'))]).id
        vals = {
            "event_id": event.get('eventid'),
            "clock": clock,
            "source": event.get('source'),
            "severity":event.get('severity'),
            "object": event.get('object'),
            "objectid": event.get('objectid'),
            "ns": event.get('ns'),
            "device": device,
            "name": event.get('name'),
            "acknowledged": event.get('acknowledged'),
            "userid": event.get("userid"),
            "suppressed": event.get("suppressed")
        }
        record = self.env['zabbix.event'].create(vals)
        return record.id


    # def sync(self):
    #     url, user, pwd = self.env['settings_configure'].get_config()
    #     print(url, user, pwd)
    #     events = ZabbixApi.event_get(url, user, pwd)
    #     for p in events:
    #         time_c = int(p.get('clock'))
    #         clock = datetime.datetime.fromtimestamp(time_c)
    #         # time_ns = int(p.get('ns'))
    #         # ns = datetime.datetime.fromtimestamp(time_ns)
    #         if len(p.get('hosts'))<1:
    #             device = ''
    #         else:
    #             host =p.get('hosts')[0]
    #             device = self.env['zabbix_host'].search([('host_id', '=', host.get('hostid'))]).id
    #             if not device:
    #                 self.env['settings_configure'].get_host_data()
    #                 device = self.env['zabbix_host'].search([('host_id', '=', host.get('hostid'))]).id
    #
    #         vals = {
    #             "event_id" : p.get('eventid'),
    #             "clock" :clock,
    #             "source":p.get('source'),
    #             "object":p.get('object'),
    #             "severity":p.get('severity'),
    #             "objectid":p.get('objectid'),
    #             "ns":p.get('ns'),
    #             "device":device,
    #             "name" : p.get('name'),
    #             "acknowledged" : p.get('acknowledged'),
    #             "r_event":p.get('r_eventid'),
    #             "userid":p.get("userid"),
    #             "suppressed":p.get("suppressed")
    #         }
    #         print(vals)
    #         rec = self.env['zabbix.event'].search([('event_id', '=', p.get('eventid'))])
    #         if rec:
    #             self.env['zabbix.event'].write(vals)
    #         else:
    #             self.env['zabbix.event'].create(vals)
    #
    #
    # def check_objects(self,objectid):
    #     if objectid == "0":
    #         return ''
    #     url, user, pwd = self.env['settings_configure'].get_config()
    #     print(url, user, pwd)
    #     record = ZabbixApi.triggergetevents(url, user, pwd,objectid)[0]
    #     rec = self.env['zabbix.event'].search([('objectid', '=', objectid),
    #                                            ('r_event','=','0'),
    #                                            ('severity','!=',"0")])
    #     if record.get('eventid') != rec.event_id:
    #         self.createvals(record)
    #     if rec:
    #         return rec.id
    #     else:
    #         rec = ZabbixApi.triggergetevents(url, user, pwd,objectid)
    #         if len(rec)<1:
    #             return ''
    #         event = rec[0]
    #         self.createvals(event)
    #
    # def createvals(self,event):
    #     time_c = int(event.get('clock'))
    #     clock = datetime.datetime.fromtimestamp(time_c)
    #     if len(event.get('hosts')) < 1:
    #         device = ''
    #     else:
    #         host = event.get('hosts')[0]
    #         device = self.env['zabbix_host'].search([('host_id', '=', host.get('hostid'))]).id
    #         if not device:
    #             self.env['zabbix.category'].sysn()
    #             device = self.env['zabbix_host'].search([('host_id', '=', host.get('hostid'))]).id
    #     vals = {
    #         "event_id": event.get('eventid'),
    #         "clock": clock,
    #         "source": event.get('source'),
    #         "severity":event.get('severity'),
    #         "object": event.get('object'),
    #         "objectid": event.get('objectid'),
    #         "ns": event.get('ns'),
    #         "device": device,
    #         "name": event.get('name'),
    #         "acknowledged": event.get('acknowledged'),
    #         "userid": event.get("userid"),
    #         "suppressed": event.get("suppressed")
    #     }
    #     record = self.env['zabbix.event'].create(vals)
    #     return record.id
    #
