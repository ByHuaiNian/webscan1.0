#coding=utf-8
#Author:huainian
#Date:2018-8-20
from django.shortcuts import render
from django.http import *
from models import *
from . import user_decorator
from plugin_app.models import Plugin_db
from project_app.models import Pro_db


def index(request):
    if request.session.get('uname'):
        return HttpResponseRedirect("/mainIndex")
    else:
        return render(request,'index_app/login.html')

#用户登录视图
def loginCheck(request):
    username = request.POST['username']
    password = request.POST['password']
    count=int(Users.objects.filter(username=username).filter(password=password).count())
    if count>0:
        request.session['uname'] = username
        request.session.set_expiry(0) #设置session过期时间为游览器关闭
    return JsonResponse({'count':count})


@user_decorator.login
def mainIndex(request):
    uname = request.session['uname']
    return render(request,'index_app/index.html',{'uname':uname})


@user_decorator.login
def mainShow(request):
    plu_count = Plugin_db.objects.count()
    pro_count = Pro_db.objects.count()
    work_count = Pro_db.objects.filter(pro_status="Pending").count()
    return render(request,'index_app/main.html',{'plu_count':plu_count,'pro_count':pro_count,'work_count':work_count})


#退出登录视图
@user_decorator.login
def logout(request):
    request.session.clear()
    return HttpResponseRedirect("/")