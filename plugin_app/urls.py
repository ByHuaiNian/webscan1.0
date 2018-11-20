#coding=utf-8
#Author:huainian
#Date:2018-8-29
from django.conf.urls import url
from . import views

urlpatterns = [
    #插件管理
    url(r'^pluginConfig$',views.pluginConfig),
    url(r'^pluginConfig_list$',views.pluginConfig_list),
    url(r'^pluginConfig_insert_show$',views.pluginConfig_insert_show),
    url(r'^pluginConfig_insert$',views.pluginConfig_insert),
    url(r'^pluginConfig_update_show$',views.pluginConfig_update_show),
    url(r'^pluginConfig_update$',views.pluginConfig_update),
    url(r'^pluginConfig_delete$',views.pluginConfig_delete),
    #应用管理
    url(r'^appConfig$',views.appConfig),
    url(r'^appConfig_list$',views.appConfig_list),
    url(r'^appConfig_insert_show$',views.appConfig_insert_show),
    url(r'^appConfig_insert$',views.appConfig_insert),
    url(r'^appConfig_update_show$',views.appConfig_update_show),
    url(r'^appConfig_update$',views.appConfig_update),
    url(r'^appConfig_del$',views.appConfig_del),
    #插件检测
    url(r'^pluginShow$',views.pluginShow),
    url(r'^pluginVerify$',views.pluginVerify),
    url(r'^pluginShow_list$',views.pluginShow_list)
]