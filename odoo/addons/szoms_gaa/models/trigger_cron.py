from odoo import models,fields,api
from odoo.exceptions import UserError

class TriggerCron(models.Model):
    _name = 'trigger.cron'


    # def sync_device(self):
    #     self.env['zabbix.category'].sync()

    def sync_event(self):
        self.env['zabbix.event'].sync()

    def open_cron(self):
        rec = self.env['ir.cron'].search([('name','=','定时获取问题事件')])
        if rec:
            raise UserError('已开启同步问题事件任务')
        model_id = self.env.ref("szoms_gaa.model_zabbix_trigger").id
        self.env['zabbix.trigger'].get_trigger()
        self.env['ir.cron'].sudo().create({
            'name': '定时获取问题事件',  # 定时任务名
            'interval_type': 'minutes',  # 定时间隔的单位
            'interval_number': 1,  # 定时间隔
            'numbercall': -1,  # 循环次数（-1代表无限循环）
            'doall': False,  # 服务器重启错过时机，是否补回执行
            'model_id': model_id,  # 任务绑定的Model
            'state': 'code',
            'code': "model.get_trigger()"
        })
