# -*- coding: utf-8 -*-

from odoo import models, fields, api
from ..controllers.controllers import ZabbixApi
from odoo.exceptions import UserError
class zabbix_group(models.Model):
    _name = 'zabbix_group'

    name = fields.Char(string="群组名", readonly=True)
    group_id = fields.Char(string="群组id", readonly=True)
    parent_id = fields.Many2one('zabbix_group', string='目录')

    def get_all_host_data(self):
        """获取配置"""
        settings_data = self.env["settings_configure"].search(
            [("url", "!=", False), ("username", "!=", False), ("password", "!=", False)])
        if not settings_data:
            raise UserError("请联系系统管理员配置url，账号，密码")
        data = ZabbixApi.get_all_host_group(settings_data.url, settings_data.username, settings_data.password)
        for this in data:
            group_data = self.search([("name", "=", this.get("name")), ("group_id", "=", this.get("groupid"))])
            if not group_data:
                data = {
                    "name": this.get("name"),
                    "group_id": this.get("groupid")
                }
                self.create(data)

class zabbix_host(models.Model):
    _name = 'zabbix_host'

    name = fields.Char(string="主机名")
    host_id = fields.Char(string="主机id")
    group_id = fields.Many2one("zabbix_group", string="所属群组")
    host_ip = fields.Char(string="ip")

    def get_host_data(self):
        settings_data = self.env["settings_configure"].search(
            [("url", "!=", False), ("username", "!=", False), ("password", "!=", False)])
        if not settings_data:
            raise UserError("请联系系统管理员配置url，账号，密码")
        for group_data in self.env["zabbix_group"].search([]):
            host = ZabbixApi.get_host(group_data.group_id, settings_data.url, settings_data.username, settings_data.password)
            if len(host["result"]) == 0:
                print("该群组下无设备")
            else:
                for host_data in host["result"]:
                    data = {
                        "name": host_data.get("name"),
                        "host_id": host_data.get("hostid"),
                        "group_id": group_data.id
                    }
                    odoo = self.env["zabbix_host"].search([("host_ip", "=", host_data.get("host"))])
                    if odoo:
                        odoo.write(data)
                    else:
                        """进入写入方法，创建主机信息"""
                        this = self.create(data)
                        this.write({"host_ip": host_data.get("host")})
                    self.env["zabbix_item_list"].search([]).create_data(host_data.get("hostid"))

    def action_view(self):
        """跳转至监控项界面"""
        action = {
            "type": "ir.actions.act_window",
            "name": "监控项",
            "res_model": "zabbix_item_list",
            "domain": [("hostid", "=", str(self.host_id))],
            "view_mode": "tree,form",
            # "target": "main"
        }
        return action

class zabbix_item_list(models.Model):
    _name = "zabbix_item_list"
    _description = "获取zabbix 监控项列表"

    name = fields.Char(string="监控项名字")
    itemid = fields.Char(string="监控项id")
    hostid = fields.Char(string="主机id")
    key = fields.Char(string="键值")
    monitor_name = fields.Char(string="关联名称")

    def create_data(self, host_id):
        """根据主机id获取监控项信息"""
        settings_data = self.env["settings_configure"].search(
            [("url", "!=", False), ("username", "!=", False), ("password", "!=", False)])
        if not settings_data:
            raise UserError("请联系系统管理员配置url，账号，密码")
        lists = ZabbixApi.get_item_list(host_id, settings_data.url, settings_data.username, settings_data.password)
        for list in lists:
            this = self.search([("hostid", "=", list.get("hostid")), ("key", "=", list.get("key_"))])
            if this:
                data = {
                    "name": list.get("name"),
                    "itemid": list.get("itemid"),
                    "hostid": list.get("hostid"),
                    "key": list.get("key_"),
                }
                this.write(data)
            else:
                data = {
                    "name": list.get("name"),
                    "itemid": list.get("itemid"),
                    "hostid": list.get("hostid"),
                    "key": list.get("key_"),
                }
                self.create(data)

    @api.model
    def create(self, vals):
        """
        重写create方法，在create方法触发后，执行定时任务
        :return:
        """
        odoo = super(zabbix_item_list, self).create(vals)
        application_item = self.env["application_item"].search([("itemid", "=", odoo.itemid)])
        if not application_item:
            application_item.create({"itemid": odoo.itemid,
                                     "hostid": odoo.hostid
                                     })
        return odoo

    def application_item(self):
        """应用该监控项为---"""
        application_item = self.env["application_item"].search([("itemid", "=", self.itemid)])
        action = {
            "type": "ir.actions.act_window",
            "name": "视图",
            "res_model": "application_item",
            "view_mode": "form",
            "target": "new",
            "res_id": application_item.id,
            "ref": "szoms_monitor.zabbix_application_item_form"
        }
        return action

    def action_view(self):
        """跳转视图且加载数据"""
        self.env["zabbix_item_data"].search([]).create_data(self.itemid)
        action = {
            "type": "ir.actions.act_window",
            "name": "监控项",
            "res_model": "zabbix_item_data",
            "domain": [("itemid", "=", str(self.itemid))],
            "view_mode": "tree,form",
        }
        return action

class zabbix_item_data(models.Model):
    """获取zabbix监控项数据"""
    _name = "zabbix_item_data"
    _order = "clock desc"

    name = fields.Char(string="监控项名字")
    itemid = fields.Char(string="监控项id", default="0")
    hostid = fields.Char(string="主机id")
    clock = fields.Char(string="时间", default="0")
    value_min = fields.Char(string="最小值", default="0")
    value_avg = fields.Char(string="平均值", default="0")
    value_max = fields.Char(string="最大值", default="0")

    def create_data(self, item_id):
        """获取监控项信息"""
        settings_data = self.env["settings_configure"].search(
            [("url", "!=", False), ("username", "!=", False), ("password", "!=", False)])
        if not settings_data:
            raise UserError("请联系系统管理员配置url，账号，密码")
        lists = ZabbixApi.get_item_data(item_id, settings_data.url, settings_data.username, settings_data.password)
        if len(lists) == 0:
            raise UserError("无监控项数据")
        for list in lists:
            odoo = self.search([("itemid", "=", list.get("itemid")), ("clock", "=", list.get("clock"))])
            if odoo:
                data = {
                    "itemid": list.get("itemid"),
                    "clock": list.get("clock"),
                    "value_min": list.get("value_min"),
                    "value_avg": list.get("value_avg"),
                    "value_max": list.get("value_max"),
                }
                odoo.write(data)
            else:
                name = ""
                hostid = ""
                for zabbix_item_data in self.search([("itemid", "=", list.get("itemid")), ("name", "!=", False)]):
                    name = zabbix_item_data.name
                    hostid = zabbix_item_data.hostid
                    break
                data = {
                    "name": name,
                    "hostid": hostid,
                    "itemid": list.get("itemid"),
                    "clock": list.get("clock"),
                    "value_min": list.get("value_min"),
                    "value_avg": list.get("value_avg"),
                    "value_max": list.get("value_max"),
                }
                self.create(data)

class application_item(models.Model):
    """应用监控项"""
    _name = "application_item"

    itemid = fields.Char(string="监控项id")
    hostid = fields.Char(string="主机id")
    name = fields.Selection([
        ("CPU", "CPU"),
        ("内存", "内存"),
        ("网络", "网络"),
        ("磁盘使用率", "磁盘使用率"),
        ("ICMP", "ICMP"),
        ("IOPS", "IOPS"),
        ("接口读写", "接口读写"),
        ("接口带宽", "接口带宽"),
        ("接口错误", "接口错误"),
        ("新建连接数", "新建连接数"),
    ], string="选择监控项", default="CPU")

    def application(self):
        """应用按钮：第一步清洗数据"""
        old_data = self.env["zabbix_item_data"].search([("name", "=", self.name), ("itemid", "!=", self.itemid),
                                                        ("hostid", "=", self.hostid)])
        if old_data:
            old_data.write({"name": False})
        """在监控列表处清除后添加标识"""
        old_zabbix_item_list = self.env["zabbix_item_list"].search([("monitor_name", "=", self.name), ("itemid", "!=", self.itemid),
                                                                ("hostid", "=", self.hostid)])
        if old_zabbix_item_list:
            old_zabbix_item_list.write({"monitor_name": False})
        """第二步：写入新的数据"""
        zabbix_item_list = self.env["zabbix_item_list"].search(
            [("itemid", "=", self.itemid)])
        zabbix_item_list.write({"monitor_name": self.name})

        zabbix_item_data = self.env["zabbix_item_data"].search([("itemid", "=", self.itemid)])
        if zabbix_item_data:
            for this in zabbix_item_data:
                this.write({"name": self.name,
                            "hostid": self.hostid
                            })
            """
            创建定时任务
            """
            cron_name = str(self.hostid) + str(self.name)
            name = self.env['ir.cron'].search([("name", "=", cron_name)])
            if not name:
                model_id = self.env.ref("szoms_monitor.model_zabbix_item_data").id
                self.env['ir.cron'].sudo().create({
                    'name': cron_name,  # 定时任务名
                    'interval_type': 'minutes',  # 定时间隔的单位
                    'interval_number': 30,  # 定时间隔
                    'numbercall': -1,  # 循环次数（-1代表无限循环）
                    'doall': False,  # 服务器重启错过时机，是否补回执行
                    'model_id': model_id,  # 任务绑定的Model
                    'state': 'code',
                    'code': "model.create_data(" + str(self.itemid) + ")"
                })
            else:
                name.write({"code": "model.create_data(" + str(self.itemid) + ")"})
            print("定时开始")
        else:
            raise UserError("请先验证历史数据是否正确")

class updateLogData(models.Model):
    """更新日志数据"""
    _name = "update_log_data"

    name = fields.Char(string="设备名称")
    update_time = fields.Char(string="更新时间")
    update_data = fields.Char(string="更新内容")
    belong = fields.Many2one("update_log", string="所属日志")

class updateLog(models.Model):
    """更新日志"""
    _name = "update_log"

    name = fields.Char(string="更新时间")
    data = fields.One2many(comodel_name="update_log_data", inverse_name="belong", string="日志内容")
