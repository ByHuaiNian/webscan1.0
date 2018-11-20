#coding=utf-8
#Author:huainian
#Date:2018-8-23
from socket import gethostbyname
from urlparse import urlparse
from config import *
import ping
import random,requests,re,os
#公共函数模块

#将url处理成标准形式 http://www.xxx.xx
def init_url(url):
    if not url.startswith('http') and not url.startswith('https'):
        url = 'http://'+url
    if url.endswith("/"):
        url = url[:-1]
    return url

#判断有些页面404 也返回200状态码的情况 发送3个404请求看状态码和页面内容长度来判断是否存在此情况
def is404(url):
    import uuid
    import string

    try:
        timeout = 10
        rand1 = ''.join(random.sample(string.ascii_letters, 8))
        rand2 = uuid.uuid4()
        rand3 = random.randint(1000000,99999999)
        user_agent = get_user_Agent()
        headers = {'User-Agent':user_agent}
        r1 = requests.get(url+"/"+str(rand1),headers=headers,timeout=timeout)
        r2 = requests.get(url+"/"+str(rand2),headers=headers,timeout=timeout)
        r3 = requests.get(url+"/"+str(rand3),headers=headers,timeout=timeout)
        if r1.status_code == r2.status_code == r3.status_code == 200 and len(r1.text) == len(r2.text) == len(r3.text):
            return len(r1.text)
        else:
            return -1
    except:
        print "404timeout"
        return -1

#随机返回一个userAgent
def get_user_Agent():
    index = random.randint(0,len(User_Agents)-1)
    return User_Agents[index]


#判断域名是否存活并获取Server和网站标题
def is_domain_success(url):
    try:
        user_agent = get_user_Agent()
        headers={'User-Agent':user_agent}
        res = requests.get(url,headers=headers,timeout=10)
        if res.status_code == 200 or res.status_code == 403 or res.status_code == 500:
            if 'Server' in res.headers:
                server = res.headers['Server']
            else:
                server = "None"
            
            text = res.content
            relist = re.findall(r'<title>(.*?)</title>',text)
            if len(relist)>0:
                title = relist[0]
            else:
                title = "None"
            return 1,(server,title)
        else:
            return -1,('None')
    except:
        return -1,('None')

#判断域名是否能ping通
def is_domain_ping(url):
    try:
        url_info = url2ip(url)
        if isinstance(url_info,tuple):
            host = str(url_info[0])
        else:
            host = str(url_info)
        pings = ping.quiet_ping(host,timeout=1)
        if pings[0] == 0:
            return 1
        else:
            return -1
    except:
        return -1


#转化url为ip
def url2ip(url):
    """
    works like turning 'http://baidu.com' => '180.149.132.47'
    """

    urlPrased = urlparse(url)
    if urlPrased.port:
        return gethostbyname(urlPrased.hostname), urlPrased.port
    return gethostbyname(urlPrased.hostname)


#获取子域名字典
def get_subdomain_dict():
    subdomain_list = []
    path = os.getcwd() + SUB_DOMAIN_DIR
    with open(path,"r") as f:
        content = f.readlines()

    for c in content:
        subdomain_list.append(c.strip())
    
    return subdomain_list

#获取下级子域名字典
def get_next_subdomain_dict():
    subdomain_list = []
    path = os.getcwd() + NEXT_SUB_DOMAIN_DIR
    with open(path,"r") as f:
        content = f.readlines()

    for c in content:
        subdomain_list.append(c.strip())
    
    return subdomain_list

#处理域名爆破url
def get_subdomain_url(domain):
    u = urlparse(domain)
    url = u.netloc
    if ":" in url:
        url = url.split(':')[0]

    url_list = url.split('.')
    end_url = ""
    for index in xrange(0,len(url_list)):
        if index == 0:
            continue
        else:
            end_url += url_list[index] + "."
    return end_url.strip(".")


#获取DNS服务器列表
def load_dns_servers():
    dns_servers = []
    path = os.getcwd()+DNS_SERVER_DIR
    with open(path,"r") as f:
        for line in f:
            server = line.strip()
            if server.count('.') == 3 and server not in dns_servers:
                dns_servers.append(server)
    return dns_servers



if __name__=='__main__':
    print init_url("www.baidu.com/")
    #print is404("http://www.sxufe.edu.cn/")