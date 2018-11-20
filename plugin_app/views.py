#coding=utf-8
#Author:huainian
#Date:2018-8-29
from django.shortcuts import render
from django.http import *
from index_app import user_decorator
from models import *
from django.core.paginator import Paginator
from pocsuite.api.cannon import Cannon
import os
from config import *
from utils import common
import json


@user_decorator.login
def pluginShow(request):
    messList = Plugin_app_db.objects.all()
    return render(request,"plugin_app/plugin_show.html",{'appList':messList})

#插件数据接口
@user_decorator.login
def pluginShow_list(request):
    app_id = request.GET.get("appid","")
    #判断是否查询应用
    if app_id!="" and app_id!="0":
        messList = Plugin_db.objects.filter(plugin_app=app_id).all()
    else:
        messList = Plugin_db.objects.all()

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
        info['plugin_name'] = m.plugin_name
        info['plugin_content'] = m.plugin_content
        info['plugin_version'] = m.plugin_version
        info['plugin_vultype'] = VUL_TYPE[m.plugin_vultype]
        info['plugin_app_name'] = m.plugin_app.app_name
        endList.append(info)
    result = {'code':0,'msg':'','count':len(messList),'data':endList}
    return JsonResponse(result)


#调用poc进行验证
@user_decorator.login
def pluginVerify(request):
    try:
        id = request.POST.get("id","")
        url = request.POST.get("url","")
        plugin_db = Plugin_db.objects.get(id=id)

        if plugin_db and url:
            plugin_dir = os.getcwd()
            plugin_dir = plugin_dir+plugin_db.plugin_filedir
            plugin_name = plugin_db.plugin_name

            #处理url
            url = common.init_url(str(url))

            info = {"pocname": str(id),
                "pocstring": open(plugin_dir).read(),
                "mode": "verify"}

            invoker = Cannon(url, info)
            result = invoker.run()

            resuList = eval(result[7]) #字符串转字典
            isSuccess = result[5]

            #设置返回信息
            info_str = ""
            for k,v in resuList.items():
                info_str += str(k)+"</br>"
                for k2,v2 in v.items():
                    info_str += str(k2)+":"+str(v2)+"</br>"


            if isSuccess[1] == "success":
                message = [1,plugin_name,info_str]
            else:
                message = [0,plugin_name,info_str]
        else:
            message = [-1,'None']
    except Exception,e:
        print e
    return JsonResponse({'data':message})


@user_decorator.login
def appConfig(request):
    return render(request,"plugin_app/plugin_app_main.html")


#应用数据接口
@user_decorator.login
def appConfig_list(request):
    messList = Plugin_app_db.objects.all()

    #分页
    page = int(request.GET.get("page","1"))
    limit = int(request.GET.get("limit","10"))

    pagin = Paginator(messList,limit)
    pageList = pagin.page(page)
    endList = []
    for m in pageList:
        info = {}
        info['id'] = m.id
        info['app_name'] = m.app_name
        endList.append(info)
    result = {'code':0,'msg':'','count':len(messList),'data':endList}
    return JsonResponse(result)

@user_decorator.login
def appConfig_insert_show(request):
    return render(request,"plugin_app/plugin_app_insert.html")

#新增应用
@user_decorator.login
def appConfig_insert(request):
    app_name = request.POST.get("appname","")
    data = 0
    if app_name!="":
        count = Plugin_app_db.objects.filter(app_name=app_name).count()
        if count==0:
            try:
                p = Plugin_app_db()
                p.app_name = app_name
                p.save()
                data = 1
            except:
                pass
    else:
        data = -1

    return JsonResponse({'data':data})


@user_decorator.login
def appConfig_update_show(request):
    id = request.GET['id']
    app = Plugin_app_db.objects.get(id=id)
    return render(request,"plugin_app/plugin_app_update.html",{'app':app})

#修改应用
@user_decorator.login
def appConfig_update(request):
    app_name = request.POST.get("appname","")
    app_id = request.POST.get("appid","")
    data = 0
    if app_name!="":
        count = Plugin_app_db.objects.filter(app_name=app_name).count()
        if count==0:
            try:
                app = Plugin_app_db.objects.get(id=app_id)
                app.app_name = app_name
                app.save()
                data = 1
            except:
                pass
    else:
        data = -1
    return JsonResponse({'data':data})

#删除应用
@user_decorator.login
def appConfig_del(request):
    id = request.POST.get("id","")
    data = 0
    if id!="":
        try:
            Plugin_app_db.objects.filter(id=id).delete()
            data = 1
        except:
            pass
    return JsonResponse({'data':data})


@user_decorator.login
def pluginConfig(request):
    messList = Plugin_app_db.objects.all()
    return render(request,"plugin_app/plugin_config_main.html",{'appList':messList})


#插件管理数据接口
@user_decorator.login
def pluginConfig_list(request):
    app_id = request.GET.get("appid","")
    #判断是否查询应用
    if app_id!="" and app_id!="0":
        messList = Plugin_db.objects.filter(plugin_app=app_id).all()
    else:
        messList = Plugin_db.objects.all()

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
        info['plugin_name'] = m.plugin_name
        info['plugin_content'] = m.plugin_content
        info['plugin_version'] = m.plugin_version
        info['plugin_vultype'] = VUL_TYPE[m.plugin_vultype]
        info['plugin_app_name'] = m.plugin_app.app_name
        endList.append(info)
    result = {'code':0,'msg':'','count':len(messList),'data':endList}
    return JsonResponse(result)

@user_decorator.login
def pluginConfig_insert_show(request):
    #获取漏洞类型
    vul_type = VUL_TYPE
    #获取应用类型
    app_list = Plugin_app_db.objects.all()
    return render(request,"plugin_app/plugin_config_insert.html",{'vul_type':vul_type,'app_list':app_list})


#新增插件
@user_decorator.login
def pluginConfig_insert(request):
    try:
        plu_name = request.POST.get("plu_name","")
        version = request.POST.get("version","None")
        if version == "":
            version = "None"
        vul_type = request.POST.get("vul_type","None")
        app_id = request.POST.get("app_id","")
        plu_content = request.POST.get("plu_content","None")
        if plu_content == "":
            plu_content = "None"
        plu_dir = request.FILES.get("plu_dir")

        data = 0
        db_dir = "/poc_plugin/"+plu_dir.name
        count = Plugin_db.objects.filter(plugin_name=plu_name).count()
        count2 = Plugin_db.objects.filter(plugin_filedir=db_dir).count()
        #判断重复
        if count==0 and count2==0:
            try:
                #上传文件
                path = os.getcwd()+"/poc_plugin/"+plu_dir.name
                with open(path,'w') as pic:
                    for c in plu_dir.readlines():
                        pic.write(c.strip("\n"))
                
                #添加数据
                plu = Plugin_db()
                plu.plugin_name = plu_name
                plu.plugin_content = plu_content
                plu.plugin_version = version
                plu.plugin_filedir = db_dir
                plu.plugin_vultype = vul_type
                plu.plugin_app = Plugin_app_db.objects.get(id=app_id)
                plu.save()
                data = 1
            except Exception,e:
                pass
    except Exception,e:
        pass

    return JsonResponse({'data':data})

@user_decorator.login
def pluginConfig_update_show(request):
    id = request.GET['id']
    #获取选中插件对象
    plu = Plugin_db.objects.get(id=id)
    #获取漏洞类型
    vul_type = VUL_TYPE
    #获取应用类型
    app_list = Plugin_app_db.objects.all()
    return render(request,"plugin_app/plugin_config_update.html",{'plu':plu,'vul_type':vul_type,'app_list':app_list})


#修改插件
@user_decorator.login
def pluginConfig_update(request):
    try:
        plu_id = request.POST.get("plu_id","")
        plu_name = request.POST.get("plu_name","")
        version = request.POST.get("version","None")
        if version == "":
            version = "None"
        vul_type = request.POST.get("vul_type","None")
        app_id = request.POST.get("app_id","")
        plu_content = request.POST.get("plu_content","None")
        if plu_content == "":
            plu_content = "None"
        plu_dir = request.FILES.get("plu_dir","")

        #获取修改对象
        plu_db = Plugin_db.objects.get(id=plu_id)

        data = 0
        #做一下判断防止报错 None值结果肯定为0
        if plu_dir == "":
            db_dir = "None"
        else:
            db_dir = "/poc_plugin/"+plu_dir.name
        count = Plugin_db.objects.filter(plugin_name=plu_name).count()
        count2 = Plugin_db.objects.filter(plugin_filedir=db_dir).count()

        #判断重复 考虑到修改时插件名称和文件时可能不修改导致和以前的名称一样 此处多加一个or判断
        if (count==0 or plu_db.plugin_name==plu_name) and (count2==0 or plu_db.plugin_filedir==db_dir):
            try:
                #判断是否上传文件
                if plu_dir != "":
                    #先删除原先的旧文件
                    old_path = os.getcwd() + plu_db.plugin_filedir
                    os.remove(old_path)

                    #上传新文件
                    path = os.getcwd()+"/poc_plugin/"+plu_dir.name
                    with open(path,'w') as pic:
                        for c in plu_dir.readlines():
                            pic.write(c.strip("\n"))
                    plu_db.plugin_filedir = db_dir
                
                #修改数据
                plu_db.plugin_name = plu_name
                plu_db.plugin_content = plu_content
                plu_db.plugin_version = version
                plu_db.plugin_vultype = vul_type
                plu_db.plugin_app = Plugin_app_db.objects.get(id=app_id)
                plu_db.save()
                data = 1
            except Exception,e:
                pass
    except Exception,e:
        pass

    return JsonResponse({'data':data})

#删除插件
@user_decorator.login
def pluginConfig_delete(request):
    id = request.POST.get("id","")
    data = 0
    if id!="":
        try:
            plu_db = Plugin_db.objects.get(id=id)

            #先删除文件
            path = os.getcwd() + plu_db.plugin_filedir
            os.remove(path)

            plu_db.delete()
            data = 1
        except:
            pass
    return JsonResponse({'data':data})