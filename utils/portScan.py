#coding=utf-8
#Author:huainian
#Date:2018-8-22
import threading
import socket
import Queue
import time


printLock = threading.Semaphore(1)

#端口扫描工具类
class PortScan():

    def __init__(self,threadSize,infoList):
        self.threadSize = int(threadSize)
        self.messList = []
        self.infoList = infoList
        self.queue = Queue.Queue()
        self.count=0

        for i in self.infoList:
            self.queue.put(i)


    def startPort(self):
        with threading.Lock():
            while not self.queue.empty():
                try:
                    tupl = self.queue.get()
                    soc=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #TCP连接
                    soc.settimeout(5)
                    ip = str(tupl[0])
                    port = int(tupl[1])
                    soc.connect((ip,port)) #向目标端口发起TCP连接
                    #soc.send("hello!this is port test!") #发送一些数据看其响应

                    #printLock.acquire()
                    print("%s port %d is open!"%(ip,port))
                    #result=soc.recv(1024)

                    self.messList.append([ip,port])
                    #printLock.release()
                    soc.close()

                except Exception,e:
                    soc.close()
                finally:
                    pass

    #开始多线程扫描端口
    def run(self):
        tList = []
        for i in xrange(self.threadSize):
            t = threading.Thread(target=self.startPort)
            tList.append(t)
            t.start()
        
        #因为使用join时可能会发生有的线程执行完 执行状态还为True 所以改为while无限循环 在列表中无值的时候再结束循环
        #加入延时是为了防止发生结果未添加进列表的bug
        while True:
            time.sleep(1)
            if self.queue.empty():
                time.sleep(5)
                break

        # isAlive = True
        # while isAlive:
        #     isAlive = False
        #     for t in tList:
        #         if t.isAlive():
        #             isAlive = True
        #             time.sleep(0.1)

        print "thread close!"
        return self.messList


