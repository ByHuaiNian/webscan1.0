#coding=utf-8
#Author:huainian
#Date:2018-9-6
from celery import Celery

app = Celery('app',include=['project_app.tasks'])
app.config_from_object('celery_config')

# useage:
# celery -A ws_celery worker -l info