#coding=utf-8
#Author:huainain
#Date:2018-8-24

from common import *
from config import *
import requests
import threading
import Queue
import time
import os

# printLock = threading.Semaphore(1)


#目录扫描类
class DirScan():


    def __init__(self,domain,threadSize,isRecursion,isKeywords,keywords,dicts,url_status):
        self.domain = domain
        self.threadSize = int(threadSize)
        self.isRecursion = isRecursion
        self.isKeywords = isKeywords
        self.keywords = keywords
        self.dicts = dicts
        self.url_status = url_status
        self.lock = threading.Lock()
        self.thread_count = self.threadSize

        #初始化url
        self.domain = init_url(self.domain)

        #获取判断值
        self.length = is404(self.domain)

        #队列
        self.queue = Queue.Queue()

        #结果集
        self.mess_list = []


    def start(self):
        with threading.Lock():
            while self.queue.qsize() > 0:
                try:
                    timeout = 10
                    user_agent = get_user_Agent()
                    headers={'User-Agent':user_agent}
                    dir = self.queue.get()
                    url = self.domain + str(dir)
                    res = requests.get(url,headers=headers,timeout=timeout)

                    status = res.status_code
                    status2 = str(status)

                    if status2 in self.url_status:
                        if self.length == -1:
                            self.mess_list.append([url,status])
                            print("[%d]===>%s"%(status,url))
                        else:
                            if len(res.text)!=self.length:
                                self.mess_list.append([url,status])
                                print("[%d]===>%s"%(status,url))
                except:
                    print("[%s]===>timeout"%(url))
            self.lock.acquire()
            self.thread_count -= 1
            self.lock.release()


    
    def run(self):
        dir_list = []
        if self.isKeywords=="1":
            dir_list = self.getKeywords_list()

        dir_list += self.getDicts()

        self.getQue(dir_list)

        for i in xrange(self.threadSize):
            t = threading.Thread(target=self.start)
            t.start()
        
        while self.thread_count > 0:
            time.sleep(1.0)
        
        print "thread close"
        return self.mess_list






    #根据关键字组合后缀形成字典
    def getKeywords_list(self):
        keywords_list = self.keywords.split(",")
        file_dir = os.getcwd() + DICT_DIR['ext']
        with open(file_dir,"r") as f:
            exts = f.readlines()
        
        dir_list=[]
        for key in keywords_list:
            for ext in exts:
                dir_list.append("/"+ext.strip().replace("$",key))

        return dir_list

    #读取字典
    def getDicts(self):
        dir_list = []
        if self.dicts[0]!="":
            for d in self.dicts:
                file_dir = os.getcwd() + DICT_DIR[d]
                with open(file_dir,"r") as f:
                    dir = f.readlines()
                
                for d in dir:
                    dir_list.append(d.strip())
        
        return dir_list


    def getQue(self,dir_list):
        for dir in dir_list:
            self.queue.put(dir)

