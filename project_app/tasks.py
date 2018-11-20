#coding=utf-8
#Author:huainian
#Date:2018-9-6
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webscan.settings")# project_name 项目名称
django.setup()
from ws_celery import app
from models import *
from plugin_app.models import Plugin_db
from utils import common,portScan,dirScan,pocScan,subDomainScan
from config import *
import requests,json,time,datetime,socket,json
import dns.resolver
import redis

redisConn = redis.Redis(host=REDIS_HOST,port=REDIS_PORT,decode_responses=True,db=REDIS_DB)

#扫描处理类
class Scan():

    def __init__(self,pro_id,domain_url_list,plu_list_id):
        self.pro_id = pro_id #项目id
        self.plu_list_id = plu_list_id #选择的插件id列表
        self.domain_url_list = domain_url_list #域名列表

    def start(self):
        scanMain.delay(self.pro_id,self.plu_list_id,self.domain_url_list)


'''
扫描思路:有一个专门处理任务的 任务总控函数 判断域名存活=>扫描子域名 然后循环每个子域名，根据判断调用各个扫描模块
域名同一扫描格式 http(s)://www.xxx.com 会处理成这样的格式 在视图时就已经处理了。poc再编写时如需ip要自行转换,带有url的验证同一开头加/
防止造成//index.html的情况，有些站会报403之类的。
网站的ip在判断域名存活时已经处理，根据url获取ip。扫端口时直接去数据库里面取就可以了
'''
#任务总控
@app.task
def scanMain(pro_id,plu_list_id,domain_url_list):
    #获取项目对象
    pro = Pro_db.objects.get(id=pro_id)

    #首先判断输入的url或url列表是否存活,并获取Server和网站标题存入数据库
    worker1_list = []
    for url in domain_url_list:
        worker1 = get_domain_info.delay(pro_id,url,"")
        worker1_list.append(worker1)
    
    #判断任务是否结束
    flag = True
    while flag:
        time.sleep(2)
        flag = False
        for w in worker1_list:
            if w.status == "PENDING":
                flag = True
    
    #扫描子域名
    if pro.pro_is_domain > 0:
        worker2 = scan_domain.delay(pro_id,domain_url_list[0])
        #等待子域名扫描完成
        flag = True
        while flag:
            time.sleep(2)
            flag = False
            if worker2.status == "PENDING":
                flag = True
    #不扫描子域名也将项目域名状态改为Finish
    else:
        pro.pro_domain_status = "Finish"
        pro.save()

    
    #获取扫描域名列表
    url_list = Domain_db.objects.filter(pro_id=pro.id)

    worker_list = []
    #如果没有选择扫描端口目录插件则直接将子域名状态更新为finish
    if pro.pro_is_port != 1 and pro.pro_is_dir != 1 and pro.pro_is_poc != 1:
        for u in url_list:
            u.domain_status = "Finish"
            u.save()
    else:
        #循环每一个域名根据判断调用扫端口，扫目录，扫插件
        for u in url_list:
            if pro.pro_is_port == 1:
                worker_port = scan_port.delay(u.id)
            else:
                worker_port = "None"
            if pro.pro_is_dir == 1:
                worker_dir = scan_dir.delay(u.id)
            else:
                worker_dir = "None"
            if pro.pro_is_poc == 1:
                worker_poc = scan_poc.delay(u.id,plu_list_id)
            else:
                worker_poc = "None"
            
            worker_list.append([worker_port,worker_dir,worker_poc,u])
        
        #根据任务完成状态更新数据库
        for w in worker_list:
            flag = True
            while flag:
                time.sleep(1)
                flag = False
                if w[0]!="None" and w[1]!="None" and w[2]!="None":
                    if w[0].status == "PENDING" or w[1].status == "PENDING" or w[2].status == "PENDING":
                        flag = True
                elif w[0]!="None" and w[1]!="None":
                    if w[0].status == "PENDING" or w[1].status == "PENDING":
                        flag = True
                elif w[0]!="None" and w[2]!="None":
                    if w[0].status == "PENDING" or w[2].status == "PENDING":
                        flag = True
                elif w[1]!="None" and w[2]!="None":
                    if w[1].status == "PENDING" or w[2].status == "PENDING":
                        flag = True
                elif w[0]!="None":
                    if w[0].status == "PENDING":
                        flag = True
                elif w[1]!="None":
                    if w[1].status == "PENDING":
                        flag = True
                elif w[2]!="None":
                    if w[2].status == "PENDING":
                        flag = True

            obj = w[3]
            obj.domain_status = "Finish"
            obj.save()

    


    # #扫描端口
    # worker3_list = []
    # if pro.pro_is_port == 1:
    #     for u in url_list:
    #         worker3 = scan_port.delay(u.id)
    #         worker3_list.append(worker3)

    # #等待扫描端口完成
    # flag = True
    # while flag:
    #     time.sleep(2)
    #     flag = False
    #     for w in worker3_list:
    #         if w.status == "PENDING":
    #             flag = True

    # #扫描目录
    # worker4_list = []
    # if pro.pro_is_dir == 1:
    #     for u in url_list:
    #         worker4 = scan_dir.delay(u.id)
    #         worker4_list.append(worker4)

    # #等待扫描目录完成
    # flag = True
    # while flag:
    #     time.sleep(2)
    #     flag = False
    #     for w in worker4_list:
    #         if w.status == "PENDING":
    #             flag = True
    # #扫描插件
    # worker5_list = []
    # if len(plu_list_id)>0:
    #     for u in url_list:
    #         worker5 = scan_poc.delay(u.id,plu_list_id)
    #         worker5_list.append(worker5)
    
    # #等待扫描插件完成
    # flag = True
    # while flag:
    #     time.sleep(2)
    #     flag = False
    #     for w in worker5_list:
    #         if w.status == "PENDING":
    #             flag = True

    #扫描完成
    proend = Pro_db.objects.get(id=pro_id)
    proend.pro_status = "Finish"
    proend.pro_end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    proend.save()


#判断域名是否存活并获取Server和网站标题
@app.task
def get_domain_info(pro_id,url,ips,flag="None"):
    pro = Pro_db.objects.get(id=pro_id)

    index,info = common.is_domain_success(url)
    if index<0:
        index2 = common.is_domain_ping(url)
    else:
        index2 = -1

    #大于0则代表存活
    if index>0 or index2>0:
        if index>0:
            server = info[0]
            title = info[1]
        elif index2>0:
            server = "None"
            title = "None"

        #处理url=>ip
        url_info = common.url2ip(url)
        if isinstance(url_info,tuple):
            host = str(url_info[0])
        else:
            host = str(url_info)
        
        ips_list = ips.split(",")

        #向数据库添加信息
        domain = Domain_db()
        domain.domain_url = url
        domain.domain_status = "Pending"
        domain.domain_title = title
        domain.domain_server = server
        if host not in ips_list:
            domain.domain_ip = host
        else:
            domain.domain_ip = ips
        #判断该项目是否扫描子域名 不扫描则 域名类型为2 扫描为0
        if pro.pro_is_domain == 0:
            domain.domain_is_one = 2
        else:
            if flag == 1:
                domain.domain_is_one = 1
            else:
                domain.domain_is_one = 0
        domain.pro_id = pro
        domain.save()




#扫描子域名任务
@app.task
def scan_domain(pro_id,domain):
    try:
        pro = Pro_db.objects.get(id=pro_id)
        # url = "http://ce.baidu.com/index/getRelatedSites?site_address="+domain
        # res = requests.get(url,timeout = 10)

        # domain_list = json.loads(res.content)
        # worker1_list = []
        # for d in domain_list['data']:
        #     url = "http://"+d['domain']
        #     worker1 = get_domain_info.delay(pro_id,url,1)
        #     worker1_list.append(worker1)


        #处理域名
        target = common.get_subdomain_url(domain)
        threads_num = SUB_DOMAIN_THREAD

        sub = subDomainScan.SubDomainScan(target,threads_num,pro.pro_is_domain)
        messList = sub.run()


        #判断域名存活
        worker3_list = []
        for m in messList:
            url = "http://"+m[0]
            ips = m[1]
            worker3 = get_domain_info.delay(pro_id,url,ips,1)
            worker3_list.append(worker3)

        flag = True
        while flag:
            time.sleep(1)
            flag = False
            for w in worker3_list:
                if w.status == "PENDING":
                    flag = True
        

        pro.pro_domain_status = "Finish"
        pro.save()

    except Exception,e:
        print e





#扫描端口
@app.task
def scan_port(domain_id):
    domain = Domain_db.objects.get(id=domain_id)
    host = domain.domain_ip
    if "," in host:
        ip = host.split(",")[0]
    else:
        ip = host
    
    #获取常用端口
    port_list = PORT_LIST
    #组合信息 (ip,port)
    info_list = []
    for p in port_list:
        info_list.append((str(ip),int(p)))
    
    #调用端口扫描工具类
    pscan = portScan.PortScan(PORT_THREAD,info_list)
    messList = pscan.run()

    #添加信息到数据库
    for mess in messList:
        p = Port_info_db()
        p.port_name = mess[1]
        p.domain_id = domain
        p.save()

#扫描目录
@app.task
def scan_dir(domain_id):
    domain = Domain_db.objects.get(id=domain_id)
    url = domain.domain_url
    #调用目录扫描工具类
    dscan = dirScan.DirScan(url,DIR_THREAD,-1,1,KEY_WORDS,['default'],['200'])
    messList = dscan.run()

    #添加信息到数据库
    for mess in messList:
        d = Dir_info_db()
        d.dir_name = mess[0]
        d.dir_status = mess[1]
        d.domain_id = domain
        d.save()

#扫描插件
@app.task
def scan_poc(domain_id,plu_list_id):
    domain = Domain_db.objects.get(id=domain_id)
    url = domain.domain_url

    poc_info = []
    for i in plu_list_id:
        plu = Plugin_db.objects.get(id=i)
        #处理列表
        poc_info.append([str(plu.id),plu.plugin_filedir,plu.plugin_name,plu.plugin_app.app_name])
    
    #调用扫描插件类
    pocscan = pocScan.PocScan(POC_THREAD,url,poc_info)
    messList = pocscan.run()

    for mess in messList:
        p = Plu_info_db()
        p.plu_name = mess[0]
        p.plu_app_type = mess[1]
        p.plu_return = mess[2]
        p.domain_id = domain
        p.save()




'''
        #处理域名
        end_domain = common.get_subdomain_url(domain)
        #获取子域名列表
        subdomain_dict = common.get_subdomain_dict()
        #获取下级域名列表
        next_subdomain_dict = common.get_next_subdomain_dict()
        #获取DNS服务器列表
        dns_servers = common.load_dns_servers()

        worker1_list = []
        messList = []
        messDict = {}
        messList_end = []
        #爆破二级域名
        for index in xrange(0,len(subdomain_dict)):
            d = end_domain.replace("$",str(subdomain_dict[index]))
            worker1 = scan_subdomain.delay(d,index,dns_servers)
            worker1_list.append(worker1)

        flag = True
        while flag:
            time.sleep(1)
            flag = False
            for w in worker1_list:
                if w.status == "PENDING":
                    flag = True
        
        #通过key去redis中取出返回值
        for w in worker1_list:
            result = redisConn.get("celery-task-meta-"+w.id)
            dicts = json.loads(result)
            if dicts['result'] != None:
                messList.append(dicts['result'])
            redisConn.delete("celery-task-meta-"+w.id)

        #过滤误报
        for m in messList:
            flag = True
            if m[1] not in messDict:
                messDict[m[1]] = 1
            else:
                messDict[m[1]] += 1
            if messDict[m[1]] > 2:
                flag = False
            if flag:
                messList_end.append((str(m[0]),str(m[1])))


        if pro.pro_is_domain == 2:
            #爆破三级域名
            worker2_list = []
            for m in messList_end:
                for index in xrange(0,len(next_subdomain_dict)):
                    d = next_subdomain_dict[index] + "." + m[0]
                    worker2 = scan_subdomain.delay(d,index,dns_servers)
                    worker2_list.append(worker2)
            
            flag = True
            while flag:
                time.sleep(1)
                flag = False
                for w in worker2_list:
                    if w.status == "PENDING":
                        flag = True
            
            messList = []
            for w in worker2_list:
                result = redisConn.get("celery-task-meta-"+w.id)
                dicts = json.loads(result)
                if dicts['result'] != None:
                    messList.append(dicts['result'])
                redisConn.delete("celery-task-meta-"+w.id)

            #过滤误报
            for m in messList:
                flag = True
                if m[1] not in messDict:
                    messDict[m[1]] = 1
                else:
                    messDict[m[1]] += 1
                if messDict[m[1]] > 2:
                    flag = False
                if flag:
                    messList_end.append((str(m[0]),str(m[1])))

        #判断域名存活
        worker3_list = []
        for m in messList_end:
            url = "http://"+m[0]
            ips = m[1]
            worker3 = get_domain_info.delay(pro_id,url,ips,1)
            worker3_list.append(worker3)

        flag = True
        while flag:
            time.sleep(1)
            flag = False
            for w in worker3_list:
                if w.status == "PENDING":
                    flag = True
        

        pro.pro_domain_status = "Finish"
        pro.save()


#爆破子域名
@app.task
def scan_subdomain(domain,index,dns_servers):
    try:
        info_list = []
        resolvers = dns.resolver.Resolver()
        resolvers.nameservers.insert(0,dns_servers[index % len(dns_servers)])
        resolvers.lifetime = resolvers.timeout = 10.0

        record = resolvers.query(domain)
        if record:
            for r in record:
                if r.address not in info_list:
                    info_list.append(r.address)
            ips = ','.join([info for info in info_list])
            return domain,ips
    except Exception,e:
        pass

'''