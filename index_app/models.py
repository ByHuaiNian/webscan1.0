#coding=utf-8
#Author:huainian
#Date:2018-8-20
from django.db import models

class Users(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

    class Meta():
        db_table='users_db'
