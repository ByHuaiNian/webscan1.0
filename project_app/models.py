#coding=utf-8
#Author:huainian
#Date:2018-9-6
from django.db import models

#项目主表
class Pro_db(models.Model):
    pro_name = models.CharField(max_length=100) #项目名称
    pro_start_time = models.CharField(max_length=50) #创建时间
    pro_end_time = models.CharField(max_length=50,null=True) #完成时间
    pro_status = models.CharField(max_length=20) #项目总状态 Finish Pending
    pro_domain_status = models.CharField(max_length=20) #域名准备 Finish Pending
    pro_is_domain = models.IntegerField(default=0) #是否扫描子域名 0不扫描 1只扫描二级域名 2扫描多级子域名 不扫描子域名时可批量扫描url
    pro_is_port = models.IntegerField(default=0) #是否扫描端口 0不扫描 1扫描
    pro_is_dir = models.IntegerField(default=0) #是否扫描目录 0不扫描 1扫描
    pro_is_poc = models.IntegerField(default=0) #是否扫描插件 0不扫描 1扫描

    class Meta():
        db_table='pro_db'


#域名表
class Domain_db(models.Model):
    domain_url = models.CharField(max_length=100) #域名
    domain_is_one = models.IntegerField() #是否是主域名 0为一级域名 1为子域名 2为批量类型
    domain_status = models.CharField(max_length=20) #完成状态 Finish Pending
    domain_title = models.CharField(max_length=100,null=True) #网站标题
    domain_server = models.CharField(max_length=50,null=True) #网站Server
    domain_ip = models.CharField(max_length=50,null=True) #网站ip
    pro_id = models.ForeignKey('Pro_db')

    class Meta():
        db_table='domain_db'


#目录表
class Dir_info_db(models.Model):
    dir_name = models.CharField(max_length=100) #路径
    dir_status = models.CharField(max_length=20) #状态码
    domain_id = models.ForeignKey('Domain_db')

    class Meta():
        db_table='dir_info_db'


#端口表
class Port_info_db(models.Model):
    port_name = models.CharField(max_length=20) #端口
    domain_id = models.ForeignKey('Domain_db')

    class Meta():
        db_table='port_info_db'


#插件扫描表
class Plu_info_db(models.Model):
    plu_name = models.CharField(max_length=100) #插件名
    plu_app_type = models.CharField(max_length=100) #插件应用类型
    plu_return = models.CharField(max_length=200) #执行返回结果
    domain_id = models.ForeignKey('Domain_db')

    class Meta():
        db_table='plu_info_db'