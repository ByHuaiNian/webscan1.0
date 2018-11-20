#coding=utf-8
#Author:huainian
#Date:2018-9-20
import dns.resolver
import threading
import Queue,time
from common import get_subdomain_dict,get_next_subdomain_dict,load_dns_servers

#子域名扫描类
class SubDomainScan():

    def __init__(self,target,threads_num,is_subdomain):
        self.target = target
        self.threads_num = self.thread_count = threads_num
        #是否扫描三级域名
        self.is_subdomain = is_subdomain
        #子域名列表
        self.subdomain_dict = get_subdomain_dict()
        #下级子域名列表
        self.next_subdomain_dict = get_next_subdomain_dict()
        #DNS服务器列表
        self.dns_servers = load_dns_servers()
        self.dns_count = len(self.dns_servers)
        #锁
        self.lock = threading.Lock()
        self.resolvers = [dns.resolver.Resolver() for _ in range(self.threads_num)]

        self.messList = []
        self.ip_dict = {}

        self.queue = Queue.Queue()
        for sub in self.subdomain_dict:
            self.queue.put(sub)

    #判断是否是私有地址
    @staticmethod
    def is_intranet(ip):
        ret = ip.split('.')
        if not len(ret) == 4:
            return True
        if ret[0] == '10':
            return True
        if ret[0] == '172' and 16 <= int(ret[1]) <= 32:
            return True
        if ret[0] == '192' and ret[1] == '168':
            return True
        return False


    def scan(self):
        thread_id = int( threading.currentThread().getName() )
        self.resolvers[thread_id].nameservers.insert(0, self.dns_servers[thread_id % self.dns_count])
        self.resolvers[thread_id].lifetime = self.resolvers[thread_id].timeout = 10.0
        while self.queue.qsize() > 0:
            try:
                sub = self.queue.get(timeout=1.0)
                self.lock.acquire()
                print  "size:" + str(self.queue.qsize())
                self.lock.release()
                cur_sub_domain = sub + '.' + self.target
                answers = self.resolvers[thread_id].query(cur_sub_domain)
                is_wildcard_record = False
                if answers:
                    for answer in answers:
                        self.lock.acquire()
                        #过滤无效地址
                        if answer.address not in self.ip_dict:
                            self.ip_dict[answer.address] = 1
                        else:
                            self.ip_dict[answer.address] += 1
                            # ip地址出现二次以上则过滤掉
                            if self.ip_dict[answer.address] > 2:
                                is_wildcard_record = True
                        self.lock.release()
                    if is_wildcard_record:
                        continue
                    ips = ', '.join([answer.address for answer in answers])
                    if not SubDomainScan.is_intranet(answers[0].address):
                        # self.lock.acquire()
                        # print  "size:" + str(self.queue.qsize())
                        # self.lock.release()
                        self.messList.append((str(cur_sub_domain),str(ips)))
                        #判断是否扫描多级域名 如果扫描则直接添加进queue队列中
                        if self.is_subdomain == 2:
                            for i in self.next_subdomain_dict:
                                self.queue.put(i + '.' + sub)
            except Exception, e:
                pass
        #在线程结束之前将 thead_count-1 为主线程判断子线程全部结束做参考
        self.lock.acquire()
        self.thread_count -= 1
        self.lock.release()

    def run(self):
        try:
            for i in range(self.threads_num):
                t = threading.Thread(target=self.scan,name=str(i))
                t.start()
            
            #如果thead_count 小于1 则代表子线程全部运行完毕
            while self.thread_count > 0:
                time.sleep(1.0)
        except Exception,e:
            pass
        
        print "thread close"
        return self.messList