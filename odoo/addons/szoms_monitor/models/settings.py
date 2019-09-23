from odoo import models, fields, api
from odoo.exceptions import UserError

class configure(models.Model):
    _name = "settings_configure"

    def default_url(self):
        url = self.env["settings_configure"].search([("url", "!=", False)]).url
        return url
    url = fields.Char(string="url配置", default=default_url)
    def default_username(self):
        username = self.env["settings_configure"].search([("username", "!=", False)]).username
        return username
    username = fields.Char(string="账号", default=default_username)
    def default_password(self):
        password = self.env["settings_configure"].search([("password", "!=", False)]).password
        return password
    password = fields.Char(string="密码", default=default_password)
    def default_group(self):
        group = self.env["settings_configure"].search([("group", "!=", False)]).group
        return group
    group = fields.Many2many("zabbix_group", string="已监控群组", default=default_group)
    def default_switch(self):
        switch = self.env["settings_configure"].search([("username", "!=", False), ("password", "!=", False)]).switch
        return switch
    switch = fields.Boolean(string="定时开关开启", default=default_switch)

    """微信配置所需字段"""
    def default_Secret(self):
        secret = self.env["settings_configure"].search([("secret", "!=", False)]).secret
        return secret
    secret = fields.Char(string="应用secret", default=default_Secret)

    def default_corpid(self):
        corpid = self.env["settings_configure"].search([("corpid", "!=", False)]).corpid
        return corpid
    corpid = fields.Char(string="企业微信id", default=default_corpid)

    def default_agentid(self):
        agentid = self.env["settings_configure"].search([("agentid", "!=", False)]).agentid
        return agentid
    agentid = fields.Char(string="应用id", default=default_agentid)

    def default_touser(self):
        touser = self.env["settings_configure"].search([("touser", "!=", False)]).touser
        return touser
    touser = fields.Char(string="微信用户", default=default_touser)

    @api.model
    def create(self, vals):
        """
        自定义瞬态模型，保存配置文件只有一条数据
        """
        this = self.env["settings_configure"].search([])
        if this:
            for record in this:
                record.unlink()
        odoo = super(configure, self).create(vals)
        return odoo

    def get_host_data(self):
        """获取群组信息"""
        self.env["zabbix_group"].get_all_host_data()
        """获取主机信息"""
        self.env["zabbix_host"].get_host_data()
        """todo：将群组关联到监控群组中"""
        ids = self.env["zabbix_group"].search([]).ids
        self.write({"group": [(6, 0, ids)]})

    def updateTime_get_host_data(self):
        """定时拉取zabbix信息"""
        if self.search([("username", "!=", False)]).switch == True:
            self.env["zabbix_group"].get_all_host_data()
            """获取主机信息"""
            self.env["zabbix_host"].get_host_data()
            """todo：将群组关联到监控群组中"""
            ids = self.env["zabbix_group"].search([]).ids
            self.write({"group": [(6, 0, ids)]})
        print("定时开启")

            # print(group_data)

    def update_time(self):
        """创建定时任务"""
        """
        创建定时任务
        """
        cron_name = "定时拉取群组数据"
        name = self.env['ir.cron'].search([("name", "=", cron_name)])
        if not name:
            model_id = self.env.ref("szoms_monitor.model_settings_configure").id
            self.env['ir.cron'].sudo().create({
                'name': cron_name,  # 定时任务名
                'interval_type': 'minutes',  # 定时间隔的单位
                'interval_number': 30,  # 定时间隔
                'numbercall': -1,  # 循环次数（-1代表无限循环）
                'doall': False,  # 服务器重启错过时机，是否补回执行
                'model_id': model_id,  # 任务绑定的Model
                'state': 'code',
                'code': "model.updateTime_get_host_data()"
            })
        print("定时")

    @api.constrains("switch")
    def get_hostgroup_data(self):
        """触发方法"""
        self.update_time()


    def get_config(self):
        config = self.search(
            [("url", "!=", False), ("username", "!=", False), ("password", "!=", False)])
        if not config:
            raise ValueError('错误，未能正确配置zabbix信息')
        return config.url,config.username,config.password

    def get_wx_data(self):
        config = self.search(
            [("secret", "!=", False), ("corpid", "!=", False), ("agentid", "!=", False), ("touser", "!=", False)])
        if not config:
            raise ValueError('错误，未能正确配置zabbix信息')

        return config.secret, config.corpid, config.agentid, config.touser

