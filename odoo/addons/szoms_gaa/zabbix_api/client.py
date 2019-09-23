import requests,json,time


class ClientException(Exception):
    pass



class ZabbixClient(object):
    def __init__(self,url,user,pwd):
        self.url = url
        self.user = user
        self.pwd = pwd
        self.auth = None
        self.header = {"Content-Type": "application/json"}



    def post(self,data):
        data['auth'] = self.check_auth()
        print(data)
        result = requests.post(self.url,headers=self.header,data=json.dumps(data))
        res = json.loads(result.content)
        if res.get('error'):
            raise ClientException("{}: {}".format(res.get('error')['code'], res.get('error')['message']))
        return res['result']


    def check_auth(self):
        if not self.auth:
            data = {
                "jsonrpc": "2.0",
                "method": "user.login",
                "params": {
                    "user": self.user,
                    "password": self.pwd
                },
                "id": 1,
                "auth": None
            }
            r = requests.post(self.url, headers=self.header, data=json.dumps(data))
            auth = json.loads(r.content)['result']
            self.auth = auth
        return self.auth

    def get_group_list(self):
        data={
            'jsonrpc': '2.0',
            'method': 'hostgroup.get',
            "params":
                {
                "output": "extend"
            },
            'auth': None,
            'id': '1'
        }
        return self.post(data)

    def get_host(self,group_id):
        data ={
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "groupids": group_id,
                "output": "extend",
            },
            "id": 2,
            "auth": None
        }
        return self.post(data)

    def get_trigger(self):
        data ={
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
            'auth': None,
            'id':'1'
            }
        return self.post(data)

    def get_problem(self):
        problem_data = {
            'jsonrpc': '2.0',
            'method': 'problem.get',
            "params":
                {
                "output": "extend",
                },
            'auth': None,
            'id':'1'
            }
        return self.post(problem_data)

    def event_get(self):
        event_data = {
            'jsonrpc': '2.0',
            'method': 'event.get',
            "params":
                {
                "output": "extend",
                "selectHosts": ["host"]
                },
            'auth': None,
            'id':'1'
            }
        return self.post(event_data)

    def eventid_get(self,eventid):
        event_data = {
            'jsonrpc': '2.0',
            'method': 'event.get',
            "params":
                {
                "output": "extend",
                "eventids":eventid,
                "selectHosts": ["host"]
                },
            'auth': None,
            'id':'1'
            }
        self.post(event_data)

    def gettrigetID(self):
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
            "auth": None,
            "id": 1
        }
        return self.post(values)

    def triggergetevents(self,triggerID):
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
            "auth": None,
            "id": 1
        }
        return self.post(values)
