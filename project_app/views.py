#coding=utf-8
#Author:huainian
#Date:2018-9-6
from django.shortcuts import render
from django.http import *
from django.core.paginator import Paginator
from tasks import *
from index_app import user_decorator
from plugin_app.models import *
from . import models,tasks
from utils import common
import json,datetime

@user_decorator.login
def projectAdd(request):
    return render(request,"project_app/project_add.html")


#插件数据接口
@user_decorator.login
def projectAdd_plulist(request):
    #tree [{'id':1,'pid':0,'name':'test','children':[{'id':1,'name':'test2'}]},{}]
    id = 1
    app_list = Plugin_app_db.objects.all()
    plu_list = []
    for app in app_list:
        plu = app.plugin_db_set.all()
        #无插件的应用不显示
        if len(plu)>0:
            objList = {}
            objList['id'] = id
            objList['name'] = app.app_name

            
            chilist = []
            for p in plu:
                chidict = {}
                chidict['id'] = p.id
                chidict['name'] = p.plugin_name
                chidict['icon'] = '/static/project_app/css/zTreeStyle/img/diy/9.png'
                chilist.append(chidict)

            objList['children'] = chilist
            plu_list.append(objList)
            id+=1
    return HttpResponse(json.dumps(plu_list))


#开始扫描
@user_decorator.login
def projectScan(request):
    try:
        data = 1
        pro_name = request.POST.get("pro_name","")
        is_domain = request.POST.get("is_domain","")
        domain_url = request.POST.get("domain_url","")
        is_port = request.POST.get("is_port","0")
        is_dir = request.POST.get("is_dir","0")
        plu_str = request.POST.get("plu_str","")

        plu_list_id = []
        if plu_str!="":
            plu_list_id = plu_str.split(",")
        
        if len(plu_list_id)>0:
            is_poc = "1"
        else:
            is_poc = "0"

        domain_url_list = []
        #是否扫描子域名
        if int(is_domain) > 0:
            domain_url_list.append(domain_url.strip())
        else:
            domain_url_list = domain_url.strip().splitlines()
        
        #处理url
        for index in xrange(len(domain_url_list)):
            domain_url_list[index] = common.init_url(domain_url_list[index])

        #将信息添加进数据库
        #项目表
        pro = Pro_db()
        pro.pro_name = pro_name
        pro.pro_start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        pro.pro_end_time = "None"
        pro.pro_status = "Pending"
        pro.pro_domain_status = "Pending"
        pro.pro_is_domain = int(is_domain)
        pro.pro_is_port = int(is_port)
        pro.pro_is_dir = int(is_dir)
        pro.pro_is_poc = int(is_poc)
        pro.save()

        #调用扫描类
        scan = Scan(pro.id,domain_url_list,plu_list_id)
        scan.start()
    except Exception,e:
        data = 0

    return JsonResponse({'data':data})


@user_decorator.login
def projectShow(request):
    return render(request,"project_app/project_show.html")


#项目列表数据接口
@user_decorator.login
def projectShow_list(request):
    try:
        #判断查询
        pro_name = request.GET.get("pro_name","")
        if pro_name != "":
            if pro_name == "all":
                messList = Pro_db.objects.all()
            else:
                messList = Pro_db.objects.filter(pro_name__icontains=pro_name)
        else:
            messList = Pro_db.objects.all()

        #分页
        page = int(request.GET.get("page","1"))
        limit = int(request.GET.get("limit","10"))

        pagin = Paginator(messList,limit)
        pageList = pagin.page(page)

        #转为json格式
        endList = []
        for m in pageList:
            info = {}
            info['id'] = m.id
            info['pro_name'] = m.pro_name
            info['pro_start_time'] = m.pro_start_time
            info['pro_end_time'] = m.pro_end_time
            if m.pro_is_domain > 0:
                info['pro_is_domain'] = "Yes"
            else:
                info['pro_is_domain'] = "No"
            info['pro_domain_status'] = m.pro_domain_status
            info['pro_status'] = m.pro_status
            endList.append(info)
        result = {'code':0,'msg':'','count':len(messList),'data':endList}
    except Exception,e:
        print e
    return JsonResponse(result)


#判断子域名是否扫描完成
@user_decorator.login
def projectShow_isdomain(request):
    id = request.POST['id']
    data = 1
    obj = Pro_db.objects.get(id=id)
    if obj.pro_domain_status == "Pending":
        data = 0
    return JsonResponse({'data':data})


@user_decorator.login
def projectShow_domain(request):
    pro_id = request.GET['id']
    pro = Pro_db.objects.get(id=pro_id)
    return render(request,"project_app/project_domain.html",{'pro':pro})


#域名列表数据接口
@user_decorator.login
def projectShow_domain_list(request):
    try:
        pro_id = request.GET['id']
        messList = Domain_db.objects.filter(pro_id=pro_id)

        #分页
        page = int(request.GET.get("page","1"))
        limit = int(request.GET.get("limit","10"))

        pagin = Paginator(messList,limit)
        pageList = pagin.page(page)

        #转为json格式
        endList = []
        for m in pageList:
            info = {}
            info['id'] = m.id
            info['domain_url'] = m.domain_url
            info['domain_title'] = m.domain_title
            info['domain_server'] = m.domain_server
            info['domain_ip'] = m.domain_ip
            info['domain_status'] = m.domain_status
            endList.append(info)
        result = {'code':0,'msg':'','count':len(messList),'data':endList}
    except Exception,e:
        print e
    return JsonResponse(result)


@user_decorator.login
def projectShow_isplu(request):
    id = request.POST['id']
    data = 1
    obj = Domain_db.objects.get(id=id)
    if obj.domain_status == "Pending":
        data = 0
    return JsonResponse({'data':data})


#扫描信息
@user_decorator.login
def projectShow_plu_info(request):
    id = request.GET['id']
    domain = Domain_db.objects.get(id=id)
    port_info = Port_info_db.objects.filter(domain_id=id)
    dir_info = Dir_info_db.objects.filter(domain_id=id)
    poc_info = Plu_info_db.objects.filter(domain_id=id)
    return render(request,"project_app/project_plu.html",{'domain':domain,'port_info':port_info,'dir_info':dir_info,'poc_info':poc_info})

#删除项目
@user_decorator.login
def projectDel(request):
    try:
        data = 1
        id = request.POST.get("id","")
        if id != "":
            pro = Pro_db.objects.get(id=id)
            pro.delete()
    except:
        data = 0
    return JsonResponse({'data':data})
