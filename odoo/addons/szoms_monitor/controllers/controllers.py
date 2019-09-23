# -*- coding: utf-8 -*-
from odoo import http
import json
import requests
from odoo.http import request

class ZabbixApi(http.Controller):
    # url = "http://172.20.65.242/zabbix/api_jsonrpc.php"
    # username = "Admin"
    # password = "zabbix"
    header = {"Content-Type": "application/json"}

    @staticmethod
    def get_token(url, username, password):
        """
        获取zabbix API token
        """
        data = {
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": username,
                "password": password
            },
            "id": 1,
            "auth": None
        }
        r = requests.post(url, headers=ZabbixApi.header, data=json.dumps(data))
        auth = json.loads(r.content)['result']
        return auth

    @staticmethod
    def get_host(group_id, url, username, password):
        """
        根据主机组id获取不同分组下的主机
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "groupids": group_id,
                "output": "extend",
            },
            "id": 2,
            "auth": ZabbixApi.get_token(url, username, password)
        })
        r = requests.post(url, headers=ZabbixApi.header, data=data)
        return json.loads(r.content)

    @staticmethod
    def get_host_group(name, url, username, password):
        """获取用户组信息"""
        group_data = {
            'jsonrpc': '2.0',
            'method': 'hostgroup.get',
            "params":
                {
                "output": "extend",
                "filter": {
                "name": [name]
                }
            },
            'auth': ZabbixApi.get_token(url, username, password),
            'id': '11'
        }
        res = requests.post(url, headers=ZabbixApi.header, data=json.dumps(group_data))
        return json.loads(res.content)['result'][0].get("groupid")

    @staticmethod
    def get_all_host_group(url, username, password):
        """获取用户组信息"""
        group_data = {
            'jsonrpc': '2.0',
            'method': 'hostgroup.get',
            "params":
                {
                "output": "extend",
            },
            'auth': ZabbixApi.get_token(url, username, password),
            'id': '11'
        }

        res = requests.post(url, headers=ZabbixApi.header, data=json.dumps(group_data))
        return json.loads(res.content)['result']


    @staticmethod
    def get_item_list(host_id, url, username, password):
        """根据host_id 获取zabbix 监控项列表"""
        data = {
            "jsonrpc": "2.0",
            "method": "item.get",
            "params": {
                "output": "extend",
                "hostids": host_id,
                "sortfield": "name"
            },
            "auth": ZabbixApi.get_token(url, username, password),
            "id": 1
        }
        res = requests.post(url, headers=ZabbixApi.header, data=json.dumps(data))
        return json.loads(res.content)['result']

    @staticmethod
    def get_item_data(items_id, url, username, password):
        """获取zabbix 监控项数据"""
        data = {
            "jsonrpc": "2.0",
            "method": "trend.get",
            "params": {
                "output": "extend",
                "itemids": items_id,
                "sortorder": "DESC",
            },
            "auth": ZabbixApi.get_token(url, username, password),
            "id": 1
        }
        res = requests.post(url, headers=ZabbixApi.header, data=json.dumps(data))
        return json.loads(res.content)['result']

    # """
    # json 格式的数据
    # """
    # @http.route('/json/list', csrf=False, auth='public')
    # def jsonList(self, **kwargs):
    #     data = request.env["zabbix_host"].search([])
    #     print(data)




