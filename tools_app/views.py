#coding=utf-8
#Author:huainian
#Date:2018-8-22
from django.shortcuts import render
from django.http import *
from index_app import user_decorator
from utils import portScan,dirScan
import time
import IPy


@user_decorator.login
def portRetu(request):
    return render(request,"tools_app/portReady.html")

@user_decorator.login
def portReady(request):
    objList = {}
    objList['ipType'] = request.POST.get("ipType","")
    objList['ips'] = request.POST.get("ips","")
    objList['threadSize'] = request.POST.get("threadSize","")
    objList['portType'] = request.POST.get("portType","")
    objList['portNumber'] = request.POST.get("portNumber","")
    return render(request,"tools_app/portShow.html",{'objList':objList})

#端口扫描操作
@user_decorator.login
def portStart(request):
    #处理参数
    ipType = request.POST['ipType']
    ips = request.POST['ips']
    threadSize = request.POST['threadSize']
    portType = request.POST['portType']
    portNumber = request.POST['portNumber']

    ipList = []
    if ipType == "1":
        ipList.append(ips)
    else:
        ipList = IPy.IP(ips)

    portList = []

    if portType == "1":
        for p in xrange(1,65536):
            portList.append(p)
    else:
        portList = portNumber.split(",")
    
    #将ip和端口整合到列表中
    endList = []
    for ip in ipList:
        for port in portList:
            endList.append((ip,port))

    #开始扫描
    p = portScan.PortScan(threadSize,endList)
    messList = p.run()

    return JsonResponse({'data':messList,'ipType':ipType})


@user_decorator.login
def dirRetu(request):
    return render(request,"tools_app/dirReady.html")


@user_decorator.login
def dirReady(request):
    import json
    objList = {}
    objList['domain'] = request.POST.get("domain","")
    objList['threadSize'] = request.POST.get("threadSize","")
    objList['isRecursion'] = request.POST.get("isRecursion","-1")
    objList['isKeywords'] = request.POST.get("isKeywords","")
    objList['keywords'] = request.POST.get("keywords","")
    objList['dicts'] = request.POST.getlist("dicts","")
    objList['dicts'] = json.dumps(objList['dicts'])
    objList['url_status'] = request.POST.getlist("url_status","")
    objList['url_status'] = json.dumps(objList['url_status'])
    return render(request,"tools_app/dirShow.html",{'objList':objList})

#目录扫描操作
@user_decorator.login
def dirStart(request):
    try:
        domain = request.POST["domain"]
        threadSize = request.POST["threadSize"]
        isRecursion = request.POST["isRecursion"]
        isKeywords = request.POST["isKeywords"]
        keywords = request.POST["keywords"]
        dicts = request.POST["dicts"]
        url_status = request.POST["url_status"]

        #因为传递列表的问题，接收的是字符串，需要做下处理
        dicts = dicts.replace('"',"")
        dicts = dicts.replace('[',"")
        dicts = dicts.replace(']',"")
        dicts = dicts.replace(' ',"")
        dicts_list = dicts.split(",")

        url_status = url_status.replace('"',"")
        url_status = url_status.replace('[',"")
        url_status = url_status.replace(']',"")
        url_status = url_status.replace(' ',"")
        url_status_list = url_status.split(",")

        #开始扫描
        d = dirScan.DirScan(domain,threadSize,isRecursion,isKeywords,keywords,dicts_list,url_status_list)
        mess_list = d.run()
    except Exception,e:
        print e

    return JsonResponse({'data':mess_list})






'''
#处理扫描端口websocket
@require_websocket
def websocket_port(request):

    #处理参数
    ipType = request.GET['ipType']
    ips = request.GET['ips']
    threadSize = request.GET['threadSize']
    portType = request.GET['portType']
    portNumber = request.GET['portNumber']

    ipList = []
    if ipType == "1":
        ipList.append(ips)
    else:
        ipList = IPy.IP(ips)

    portList = []

    if portType == "1":
        for p in xrange(1,65536):
            portList.append(p)
    else:
        portList = portNumber.split(",")


    #将ip和端口整合到队列中
    endList = []
    que = Queue.Queue()
    for ip in ipList:
        for port in portList:
            que.put((ip,port))

    #扫描处理
    messList=[] #消息列表
    tlist=[]
    start = len(messList)

    for tj in xrange(0,int(threadSize)):
        tj=portScan.PortScan(que,messList)
        tj.start()
        tlist.append(tj)
    
    try:
        #循环来接收扫描结果 并向前端发送
        while True:
            flag = False
            time.sleep(1)

            end = len(messList)

            if end>start:
                start = end
                res = {"endList":messList,"status":"1"}
                result = json.dumps(res).encode()
                print result
                request.websocket.send(result)

            for t in tlist:
                if not t.is_alive():
                    flag=True
            
            if que.empty() and flag==True:
                time.sleep(3)
                res = {"endList":messList,"status":"2"}
                result = json.dumps(res).encode()
                request.websocket.send(result)
                message = request.websocket.wait()
                if message is None:
                    break
    except Exception,e:
        pass
'''