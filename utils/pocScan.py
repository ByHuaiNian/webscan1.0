#coding=utf-8
#Author:huainian
#Date:2018-9-14
import threading
import Queue
import time
import os,json
from pocsuite.api.cannon import Cannon
printLock = threading.Semaphore(1)

class PocScan():

    def __init__(self,threadSize,url,poc_info):
        self.threadSize = threadSize
        self.url = url
        self.poc_info = poc_info #[[poc_id,poc_dir,poc_name,poc_type],]
        self.messList = []

        #处理路径
        plugin_dir = os.getcwd()
        for info in self.poc_info:
            path = plugin_dir + info[1]
            info[1] = path

        self.queue = Queue.Queue()
        for info2 in self.poc_info:
            self.queue.put(info2)


    def start(self):
        with threading.Lock():
            while not self.queue.empty():
                try:
                    poc = self.queue.get()

                    id = poc[0]
                    path = poc[1]
                    plu_name = poc[2]
                    plu_type = poc[3]

                    info = {"pocname": id,
                        "pocstring": open(path).read(),
                        "mode": "verify"}

                    invoker = Cannon(self.url, info)
                    result = invoker.run()

                    resuList = eval(result[7]) #字符串转字典
                    isSuccess = result[5]

                    if isSuccess[1] == "success":
                        #设置返回信息
                        info_str = ""
                        for k,v in resuList.items():
                            info_str += str(k)+"|"
                            for k2,v2 in v.items():
                                info_str += str(k2)+":"+str(v2)+"|"

                        self.messList.append([plu_name,plu_type,info_str])
                except Exception,e:
                    pass
    
    def run(self):
        tList = []
        for i in xrange(self.threadSize):
            t = threading.Thread(target=self.start)
            tList.append(t)
            t.start()
        

        while True:
            time.sleep(1)
            if self.queue.empty():
                time.sleep(20)
                break

        print "thread close!"
        return self.messList


if __name__=='__main__':
    test = [['1','/poc_plugin/zabixx_303_sql.py','zabbixsql','zabbix'],['2','/poc_plugin/zabbix_303_sql_getinfo.py','zabbixsqlget','zabbix']]
    p = PocScan(5,'http://89.239.138.140:5001/',test)
    l=p.run()
    print l