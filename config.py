#coding=utf-8
#Author:huainian
#Date:2018-8-23

#配置文件

#redis配置信息
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_DB = 1 #这里指定的数据库是接收返回值的，要跟celery_config.py中的CELERY_RESULT_BACKEND对应

#字典路径
DICT_DIR={
    'asp':'/dict/asp.txt',
    'aspx':'/dict/aspx.txt',
    'jsp':'/dict/jsp.txt',
    'php':'/dict/php.txt',
    'dir':'/dict/dir.txt',
    'pack':'/dict/pack.txt',
    'ext':'/dict/ext.txt',
    'default':'/dict/default.txt'
}

#二级子域名字典
SUB_DOMAIN_DIR='/dict/domain_next.txt'

#多级子域名字典
NEXT_SUB_DOMAIN_DIR='/dict/domain3.txt'

#DNS服务器路径
DNS_SERVER_DIR='/dict/dns_servers.txt'



#漏洞类型
VUL_TYPE={
    'Cross Site Scripting':'跨站脚本',
    'Cross Site Request Forgery':'跨站请求伪造',
    'SQL Injection':'Sql注入',
    'LDAP Injection':'ldap注入',
    'Mail Command Injection':'邮件命令注入',
    'Null Byte Injection':'空字节注入',
    'CRLF Injection':'CRLF注入',
    'SSI Injection':'Ssi注入',
    'XPath Injection':'Xpath注入',
    'XML Injection':'Xml注入',
    'XQuery Injection':'Xquery 注入',
    'Command Execution':'命令执行',
    'Code Execution':'代码执行',
    'Remote File Inclusion':'远程文件包含',
    'Local File Inclusion':'本地文件包含',
    'Brute Force':'暴力破解',
    'Buffer Overflow':'缓冲区溢出',
    'Credential Prediction':'证书预测',
    'Session Prediction':'会话预测',
    'Denial of Service':'拒绝服务',
    'Fingerprinting':'指纹识别',
    'URL Redirector Abuse':'url重定向',
    'Privilege Escalation':'权限提升',
    'Arbitrary File Creation':'任意文件创建',
    'Arbitrary File Download':'任意文件下载',
    'Arbitrary File Deletion':'任意文件删除',
    'Backup File Found':'备份文件发现',
    'Database Found':'数据库发现',
    'Directory Listing':'目录遍历',
    'Directory Traversal':'目录穿越',
    'File Upload':'文件上传',
    'Login Bypass':'登录绕过',
    'Weak Password':'弱密码',
    'Remote Password Change':'远程密码修改',
    'Code Disclosure':'代码泄漏',
    'Path Disclosure':'路径泄漏',
    'Information Disclosure':'信息泄漏',
    'Unauthorized Access':'未授权访问',
    'Security Mode Bypass':'安全模式绕过',
    'Malware':'挂马',
    'Black Link':'暗链',
    'Backdoor':'后门'
}

#项目扫描常用端口
PORT_LIST=[21,22,23,25,53,80,110,139,143,389,443,445,465,873,993,995,1080,1099,1311,1723,1433,1521,2181,3000,3001,3002,3306,3389,3690,4000,5432,5900,6379,7001,8000,8001,8080,8081,8161,8888,9200,9300,9080,9090,9999,11211,27017]

#项目扫描目录自定义关键词
KEY_WORDS="admin,ctf,login,manage"

#子域名扫描线程数
SUB_DOMAIN_THREAD=60

#项目扫端口线程
PORT_THREAD = 5

#项目扫目录线程
DIR_THREAD = 5

#扫插件线程
POC_THREAD = 5


#Users-Agents
User_Agents=[
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; de-LI; rv:1.9.0.16) Gecko/2009120208 Firefox/3.0.16 (.NET CLR 3.5.30729)',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.0.2pre) Gecko/2008082305 Firefox/3.0.2pre',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.2) Gecko/20100316 Firefox/3.6.2 ( .NET CLR 3.0.04506.648)',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.197.11 Safari/532.0',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.208.0 Safari/532.0',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.19 (KHTML, like Gecko) Chrome/11.0.661.0 Safari/534.19',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.21 (KHTML, like Gecko) Chrome/11.0.682.0 Safari/534.21',
    'Mozilla/5.0 (Windows NT 5.1; U; Firefox/3.5; en; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 Opera 10.53',
    'Mozilla/5.0 (Windows NT 5.1; U; Firefox/4.5; en; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 Opera 10.53',
    'Mozilla/5.0 (Windows NT 5.1; U; Firefox/5.0; en; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 Opera 10.53',
    'Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.9a1) Gecko/20061204 Firefox/3.0a1',
    'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_4_11; nl-nl) AppleWebKit/533.16 (KHTML, like Gecko) Version/4.1 Safari/533.16',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en-US; rv:1.8.1) Gecko/20061024 Firefox/2.0',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en-US; rv:1.8.0.7) Gecko/20060909 Firefox/1.5.0.7',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en-US; rv:1.8.0.6) Gecko/20060728 Firefox/1.5.0.6',
    'Mozilla/5.0 (X11; U; CrOS i686 0.9.128; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.552.339',
    'Mozilla/5.0 (X11; U; CrOS i686 0.9.128; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.552.343 Safari/534.10',
    'Mozilla/5.0 (X11; U; FreeBSD i386; de-CH; rv:1.9.2.8) Gecko/20100729 Firefox/3.6.8',
    'Mozilla/5.0 (X11; U; FreeBSD i386; en-US; rv:1.9a2) Gecko/20080530 Firefox/3.0a2',
    'Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US) AppleWebKit/530.7 (KHTML, like Gecko) Chrome/2.0.175.0 Safari/530.7',
    'Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.202.2 Safari/532.0',
    'Mozilla/5.0 (X11; U; Linux i686; de; rv:1.9.0.12) Gecko/2009070811 Ubuntu/9.04 (jaunty) Firefox/3.0.12',
    'Mozilla/5.0 (X11; U; Linux i686; de; rv:1.9.0.13) Gecko/2009080315 Ubuntu/9.04 (jaunty) Firefox/3.0.13',
    'Mozilla/5.0 (X11; U; Linux i686; de; rv:1.9.0.14) Gecko/2009082505 Red Hat/3.0.14-1.el5_4 Firefox/3.0.14',
    'Mozilla/5.0 (X11; U; Linux i686; de; rv:1.9.0.2) Gecko/2008092313 Ubuntu/8.04 (hardy) Firefox/3.0.2',
    'Mozilla/5.0 (X11; U; Linux i686; de; rv:1.9.2.10) Gecko/20100915 Ubuntu/9.10 (karmic) Firefox/3.6.10',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_5_8) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.68 Safari/534.24',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X; U; en; rv:1.8.0) Gecko/20060728 Firefox/1.5.0 Opera 9.27',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.7; en-US; rv:1.9.2.2) Gecko/20100316 Firefox/3.6.2'
]
