from odoo import models,fields,api
from email.mime.text import MIMEText
import smtplib
import requests

class ZabbixAlarm(models.Model):
    _name = 'zabbix.alarm'

    name = fields.Char('告警配置名')
    priority = fields.Selection([('0', '未分类'),
                                 ('1', '信息'),
                                 ('2', '警告'),
                                 ('3', '平均'),
                                 ('4', '高'),
                                 ('5', '灾难')], string='优先级',requird=True)
    interval_number = fields.Integer('告警间隔',required=True)
    interval_type = fields.Selection([('minutes', '分钟'),
                                 ('hours', '小时'),
                                 ('days', '天')],string='告警时间单位',required=True)
    recive_user = fields.Many2one('res.users','接收人')
    types = fields.Selection([('wechart','微信'),('email','邮件'),('phone','电话')],string='推送方式',required=True)




class AlarmEvent(models.Model):
    _name = 'alarm.event'

    name = fields.Char('定时告警任务')
    cron = fields.Many2one('ir.cron','关联任务')
    event_id = fields.Many2one('zabbix.event', '触发器事件')
    content = fields.Char('描述信息',related="event_id.name")
    severity = fields.Selection([('0', '未分类'),
                                 ('1', '信息'),
                                 ('2', '警告'),
                                 ('3', '平均'),
                                 ('4', '高'),
                                 ('5', '灾难')], string='严重程度',related="event_id.severity")
    types = fields.Selection([('wechart', '微信'), ('email', '邮件'), ('phone', '电话')],'通知方式')
    recive_user = fields.Many2one('res.users', '接收人')
    email = fields.Char('邮箱',related='recive_user.email')

    def create_event(self,vals):
        print('创建告警任务')
        rec = self.env['zabbix.alarm'].search([('priority','=',vals.get('priority'))])
        print(rec.types)
        if rec:
            name = str(vals.get("trigger_id")) + '事件推送任务'
            model_id = self.env.ref("szoms_gaa.model_alarm_event").id
            cron = self.env['ir.cron'].sudo().create({
                'name': name,  # 定时任务名
                'interval_type': rec.interval_type,  # 定时间隔的单位
                'interval_number': rec.interval_number,  # 定时间隔
                'numbercall': -1,  # 循环次数（-1代表无限循环）
                'doall': False,  # 服务器重启错过时机，是否补回执行
                'model_id': model_id,  # 任务绑定的Model
                'state': 'code'
            })
            values = {
                'name':name,
                'cron':cron.id,
                'event_id':vals.get('trigger_id'),
                'types':rec.types,
                'recive_user':rec.recive_user.id
            }
            print(values)
            event = self.env['alarm.event'].create(values)
            cron.write({
                "code": "model.send_mission(" + str(event.id) + ")"
            })
            self.send_mission(event.id)
        else:
            pass


    def send_mission(self,id):
        print('推送消息')
        record = self.env['alarm.event'].search([('id','=',id)])
        print(record.types)
        if record.types == 'wechart':
            content = '运维系统出现%s紧急程度的告警，具体事件为%s'%(record.severity,record.content)
            self.send_wechart(content)
        if record.types == 'email':
            try:
                print(record.email)
                print(record.content)
                title = '运维系统出现%s紧急程度'%record.severity
                print(title)
                self.sed_email(record.email,title,record.content)
            except:
                raise UserWarning('由于未知原因未能成功发送邮件，请联系系统管理员')

        if record.types == 'phone':
            pass

    @staticmethod
    def sed_email(email, title, content):
        msg_from = '1049449047@qq.com'  # 发送方邮箱
        passwd = 'dicmqiomeptqbdeb'  # 填入发送方邮箱的授权码
        msg_to = email  # 收件人邮箱

        subject = title  # 主题
        content = content
        msg = MIMEText(content)
        msg['Subject'] = subject
        msg['From'] = msg_from
        msg['To'] = msg_to
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login(msg_from, passwd)
        s.sendmail(msg_from, msg_to, msg.as_string())
        s.quit()

    def send_wechart(self, content):
        secret, cropid, agentid, touser = self.env["settings_configure"].get_wx_data()
        print(self.env["settings_configure"].get_wx_data())
        Secret = secret
        corpid = cropid
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}'
        getr = requests.get(url=url.format(corpid, Secret))
        access_token = getr.json().get('access_token')

        data = {
            "touser": touser,
            # "touser": "用户账号1|用户账户2",  # 向这些用户账户发送
            # "toparty" : "PartyID1|PartyID2",   # 向这些部门发送
            "msgtype": "text",
            "agentid": agentid,  # 应用的 id 号
            "text": {
                "content": content
            },
            "safe": 0
        }
        import json
        r = requests.post(url="https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}".format(access_token),
                          data=json.dumps(data))
        print(json.loads(r.content))

