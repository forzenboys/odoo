import requests,json,time

class ZabbixApi():
    # url = "http://172.20.65.242/zabbix/api_jsonrpc.php"
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
                "password":password
            },
            "id": 1,
            "auth": None
        }
        r = requests.post(url, headers=ZabbixApi.header, data=json.dumps(data))
        auth = json.loads(r.content)['result']
        return auth

    @staticmethod
    def get_host(url,username, password,group_id):
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
            "auth": ZabbixApi.get_token(url,username, password)
        })
        r = requests.post(url, headers=ZabbixApi.header, data=data)
        return json.loads(r.content)['result']

    @staticmethod
    def get_group_list(url,username, password):
        """获取所有用户组信息"""
        group_data = {
            'jsonrpc': '2.0',
            'method': 'hostgroup.get',
            "params":
                {
                "output": "extend"
            },
            'auth': ZabbixApi.get_token(url,username, password),
            'id': '1'
        }

        res = requests.post(url, headers=ZabbixApi.header, data=json.dumps(group_data))
        return json.loads(res.content)['result']


    @staticmethod
    def get_host_group(url,username, password,name):
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
            'auth': ZabbixApi.get_token(url,username, password),
            'id': '11'
        }

        res = requests.post(url, headers=ZabbixApi.header, data=json.dumps(group_data))
        print(res)
        print(res.status_code)
        print(json.loads(res.content)['result'][0].get("groupid"))
        return json.loads(res.content)['result'][0].get("groupid")

    @staticmethod
    def get_trigger(url,username, password):
        alert_data = {
            'jsonrpc': '2.0',
            'method': 'trigger.get',
            "params":
                {
                "output": "extend",
                # "output": ["triggerid","description","priority","status","value","lastchange","recovery_mode","hosts","state"],
                "filter": {
                    "value" : 1
                },
                "sortfield" : "priority",
                "sortorder" :"DESC",
                "selectHosts":["host"],
                "selectGroups":["group"]
                },
            'auth': ZabbixApi.get_token(url,username, password),
            'id':'1'
            }
        res = requests.post(url, headers=ZabbixApi.header, data=json.dumps(alert_data))
        print(json.loads(res.content)['result'])
        return json.loads(res.content)['result']

    @staticmethod
    def get_problem(url,username, password):
        problem_data = {
            'jsonrpc': '2.0',
            'method': 'problem.get',
            "params":
                {
                "output": "extend",
                },
            'auth': ZabbixApi.get_token(url,username, password),
            'id':'1'
            }
        res = requests.post(url,headers=ZabbixApi.header,data=json.dumps((problem_data)))
        return json.loads(res.content)['result']

    @staticmethod
    def event_get(url,username, password):
        event_data = {
            'jsonrpc': '2.0',
            'method': 'event.get',
            "params":
                {
                "output": "extend",
                "selectHosts": ["host"]
                },
            'auth': ZabbixApi.get_token(url,username, password),
            'id':'1'
            }
        res = requests.post(url,headers=ZabbixApi.header,data=json.dumps(event_data))
        return json.loads(res.content)['result']

    @staticmethod
    def eventid_get(url,username, password,eventid):
        event_data = {
            'jsonrpc': '2.0',
            'method': 'event.get',
            "params":
                {
                "output": "extend",
                "eventids":eventid,
                "selectHosts": ["host"]
                },
            'auth': ZabbixApi.get_token(url,username, password),
            'id':'1'
            }
        res = requests.post(url,headers=ZabbixApi.header,data=json.dumps(event_data))
        return json.loads(res.content)['result']

    @staticmethod
    def gettrigetID(url,username, password):
        values = {
            "jsonrpc": "2.0",
            "method": "trigger.get",
            "params": {
                "output": ['triggerid','description','status','priority','lastchange','hosts','state'],
                "filter": {
                    "value": 1
                },
                "selectHosts": ["host"],
                "sortfield": "priority",
                "sortorder": "DESC"
            },
            "auth": ZabbixApi.get_token(url,username, password),
            "id": 1
        }
        output = requests.post(url,headers=ZabbixApi.header,data=json.dumps(values))
        return json.loads(output.content)['result']


    # 触发器检索事件,返回一系列以事件为元素的列表。
    @staticmethod
    def triggergetevents(url,username, password,triggerID):
        values = {
            "jsonrpc": "2.0",
            "method": "event.get",
            "params": {
                "output": "extend",
                "select_acknowledges": "extend",
                "objectids": triggerID,
                "sortfield": ["clock", "eventid"],
                "sortorder": "DESC",
                "selectHosts": ["host"]
            },
            "auth": ZabbixApi.get_token(url,username, password),
            "id": 1
        }
        output = requests.post(url,headers=ZabbixApi.header,data=json.dumps(values))
        return json.loads(output.content)['result']

    #
    # # 按时间检索事件
    # def timegetevents(time_from, time_till, url, auth):
    #     values = {
    #         "jsonrpc": "2.0",
    #         "method": "event.get",
    #         "params": {
    #             "output": "extend",
    #             "time_from": time_from,
    #             "time_till": time_till,
    #             "sortfield": ["clock", "eventid"],
    #             "sortorder": "desc"
    #         },
    #         "auth": auth,
    #         "id": 1
    #     }
    #     output = requestJson(url, values)
    #     return output
    #
    #
    # # 通过eventID查询事件
    # def eventget(eventid, url, auth):
    #     values = {
    #         "jsonrpc": "2.0",
    #         "method": "event.get",
    #         "params": {
    #             "output": ["eventid", "acknowledged", "objectid"],
    #             "select_acknowledges": ["eventid", "message", "action", "alias"],
    #             "eventids": eventid,
    #         },
    #         "auth": auth,
    #         "id": 1
    #     }
    #     output = requestJson(url, values)
    #     return output


    # 定义确认事件方法
    @staticmethod
    def eventackknowledge(url,username, password,eventid,message,action=0):
        values = {
            'jsonrpc': '2.0',
            'method': 'event.acknowledge',
            'params': {
                'eventids': eventid,
                'message': message,
                'action': action
            },
            'auth':ZabbixApi.get_token(url,username, password),
            'id': 1
        }

        output = requests.post(url, headers=ZabbixApi.header, data=json.dumps(values))
        return json.loads(output.content)['result']



    # # 通过动作ID检索警报
    # def actionidgetalert(url, auth):
    #     values = {
    #         "jsonrpc": "2.0",
    #         "method": "alert.get",
    #         "params": {
    #             "output": "extend",
    #             "actionids": '7'
    #         },
    #         "auth": auth,
    #         "id": 1
    #     }
    #     output = requestJson(url, values)
    #     return output
    #
    #
    # # 定义更新action函数
    # def mediatypeupdate(mediatypeid, status, auth):
    #     values = {'jsonrpc': '2.0',
    #               'method': 'mediatype.update',
    #               'params': {
    #                   "mediatypeid": mediatypeid,
    #                   "status": status
    #               },
    #               'auth': auth,
    #               'id': '1'
    #               }
    #     output = requestJson(url, values)
    #
    #
    # # 定义读取状态函数
    # def triggerget(auth):
    #     values = {'jsonrpc': '2.0',
    #               "method": "trigger.get",
    #               "params": {
    #                   "output": [
    #                       "triggerid",
    #                       "description",
    #                       "priority"
    #                   ],
    #                   "filter": {
    #                       "value": 1
    #                   },
    #                   "expandData": "hostname",
    #                   "sortfield": "priority",
    #                   "sortorder": "DESC"
    #               },
    #               'auth': auth,
    #               'id': '2'
    #               }
    #     output = requestJson(url, values)
    #     return output
    #
    #
    # # 定义通过ip获取主机id的函数
    # def ipgetHostsid(ip, url, auth):
    #     values = {'jsonrpc': '2.0',
    #               'method': 'host.get',
    #               'params': {
    #                   'output': ["host"],
    #                   'filter': {
    #                       'ip': ip
    #                   },
    #               },
    #               'auth': auth,
    #               'id': '3'
    #               }
    #     output = requestJson(url, values)
    #     return output
    #
    #
    # # 定义通过主机id获取开启关闭监控函数
    # def idupdatehost(status, hostid, url, auth):
    #     values = {'jsonrpc': '2.0',
    #               'method': 'host.update',
    #               'params': {
    #                   "hostid": hostid,
    #                   "status": status
    #               },
    #               'auth': auth,
    #               'id': '4'
    #               }
    #     output = requestJson(url, values)
    #     return output
    #
    #
    # # 定义通过项目hostid获取itemid函数
    # def getHostsitemsid(hostid, itemsname, url, auth):
    #     values = {'jsonrpc': '2.0',
    #               'method': "item.get",
    #               "params": {
    #                   "output": ["itemids"],
    #                   "hostids": hostid,
    #                   "filter": {
    #                       "key_": itemsname,
    #                   },
    #               },
    #
    #               'auth': auth,
    #               'id': '5'
    #               }
    #     output = requestJson(url, values)
    #     if len(output) == 0:
    #         return output
    #     else:
    #         return output[0]['itemid']
    #
    #
    # # 定义通过项目id获取监控项目最近值信息的函数
    # def getHostsitemsvalue(itemid, url, auth):
    #     values = {'jsonrpc': '2.0',
    #               'method': "history.get",
    #               "params": {
    #                   "output": "extend",
    #                   "history": 3,
    #                   "itemids": itemid,
    #                   "sortfield": "clock",
    #                   "sortorder": "DESC",
    #                   "limit": 1,
    #               },
    #
    #               'auth': auth,
    #               'id': '6'
    #               }
    #     output = requestJson(url, values)
    #     if len(output) == 0:
    #         return output
    #     else:
    #         return output[0]["value"]
    #
    #
    # # 定义更新读取状态action函数
    # def mediatypeget(mediatypeid, auth):
    #     values = {'jsonrpc': '2.0',
    #               'method': 'mediatype.get',
    #               'params': {
    #                   "output": "extend",
    #
    #                   "filter": {
    #                       "mediatypeid": mediatypeid,
    #                   },
    #               },
    #
    #               'auth': auth,
    #               'id': '7'
    #               }
    #     output = requestJson(url, values)
    #     if len(output) == 0:
    #         return output
    #     else:
    #         return output[0]['status']
    #
    #
    # # 定义maintenance维修模式host函数
    # def maintenancecreate(maintenancename, active_since, active_till, hostid, auth):
    #     values = {'jsonrpc': '2.0',
    #               'method': 'maintenance.create',
    #               'params': {
    #                   "name": maintenancename,
    #                   "active_since": active_since,
    #                   "active_till": active_till,
    #                   "hostids": [
    #                       hostid
    #                   ],
    #                   "timeperiods": [
    #                       {
    #                           "timeperiod_type": 0,
    #                           "every": 1,
    #                           "dayofweek": 64,
    #                           "start_time": 64800,
    #                           "period": 3600
    #                       }
    #                   ]
    #               },
    #               'auth': auth,
    #               'id': '8'
    #               }
    #     output = requestJson(url, values)
    #
    #
    # # 定义通过模糊获取关闭主机信息函数
    # def disabledhostget(url, auth):
    #     values = {'jsonrpc': '2.0',
    #               'method': 'host.get',
    #               "params": {
    #                   "output": ["host"],
    #                   'selectInterfaces': ["ip"],
    #                   "filter": {
    #                       "status": 1
    #                   }
    #               },
    #               'auth': auth,
    #               'id': '9'
    #               }
    #     output = requestJson(url, values)
    #     return output
    #
    #
    # # 定义maintenance维修模式group函数
    # def maintenancecreategroup(maintenancename, active_since, active_till, groupid, auth):
    #     values = {'jsonrpc': '2.0',
    #               'method': 'maintenance.create',
    #               'params': {
    #                   "name": maintenancename,
    #                   "active_since": active_since,
    #                   "active_till": active_till,
    #                   "groupids": [
    #                       groupid
    #                   ],
    #                   "timeperiods": [
    #                       {
    #                           "timeperiod_type": 0,
    #                           "every": 1,
    #                           "dayofweek": 64,
    #                           "start_time": 64800,
    #                           "period": 3600
    #                       }
    #                   ]
    #               },
    #               'auth': auth,
    #               'id': '10'
    #               }
    #     output = requestJson(url, values)
    #
    #
    # # 定义通过host groups named 获取groupid
    # def groupnameGroupid(groupname, auth):
    #     values = {'jsonrpc': '2.0',
    #               'method': 'hostgroup.get',
    #               "params": {
    #                   "output": "extend",
    #                   "filter": {
    #                       "name": [
    #                           groupname
    #                       ]
    #                   }
    #               },
    #               'auth': auth,
    #               'id': '11'
    #               }
    #     output = requestJson(url, values)
    #     return output
    #
    #
    # # 定义模糊查询维护主机
    # def maintenanceget(url, auth):
    #     values = {'jsonrpc': '2.0',
    #               'method': 'maintenance.get',
    #               "params": {
    #                   "output": "extend",
    #               },
    #               'auth': auth,
    #               'id': '12'
    #               }
    #     output = requestJson(url, values)
    #     return output
    #
    #
    # # 定义批量恢复处于维护主机
    # def maintenancedelete(maintenanceid, url, auth):
    #     values = {'jsonrpc': '2.0',
    #               'method': 'maintenance.delete',
    #               "params": [
    #                   maintenanceid
    #               ],
    #               'auth': auth,
    #               'id': '13'
    #               }
    #     output = requestJson(url, values)
    #     return output
    #
    #
    # # 定义通过hostid获取graphid的函数
    # def getgraphid(hostid, graphname, url, auth):
    #     values = {'jsonrpc': '2.0',
    #               'method': 'graph.get',
    #               'params': {
    #                   "output": "name",
    #                   "hostids": hostid,
    #                   "sortfield": "name",
    #                   'filter': {
    #                       "name": graphname
    #                   },
    #
    #               },
    #               'auth': auth,
    #               'id': '14'
    #               }
    #     output = requestJson(url, values)
    #     return output