#coding=utf-8
#Author:huainian
#Date:2018-9-6
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^projectAdd$',views.projectAdd),
    url(r'^projectAdd_plulist$',views.projectAdd_plulist),
    url(r'^projectScan$',views.projectScan),
    url(r'^projectShow$',views.projectShow),
    url(r'^projectShow_list$',views.projectShow_list),
    url(r'^projectShow_isdomain$',views.projectShow_isdomain),
    url(r'^projectShow_domain$',views.projectShow_domain),
    url(r'^projectShow_domain_list$',views.projectShow_domain_list),
    url(r'^projectShow_isplu$',views.projectShow_isplu),
    url(r'^projectShow_plu_info$',views.projectShow_plu_info),
    url(r'^projectDel$',views.projectDel)
]