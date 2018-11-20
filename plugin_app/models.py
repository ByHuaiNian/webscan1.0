#coding=utf-8
#Author:huainian
#Date:2018-8-29
from django.db import models

class Plugin_db(models.Model):
    plugin_name = models.CharField(max_length=100) #插件名称
    plugin_content = models.CharField(max_length=200,null=True) #插件说明
    plugin_version = models.CharField(max_length=100,null=True) #影响版本
    plugin_filedir = models.CharField(max_length=100) #文件路径
    plugin_vultype = models.CharField(max_length=100,null=True) #漏洞类型
    plugin_app = models.ForeignKey('Plugin_app_db') #应用id


    class Meta():
        db_table='plugin_db'



class Plugin_app_db(models.Model):
    app_name = models.CharField(max_length=100)

    class Meta():
        db_table='plugin_app_db'