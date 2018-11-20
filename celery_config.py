#coding=utf-8
#Author:huainian
#Date:2018-9-6
from kombu import Exchange,Queue

BROKER_URL = "redis://127.0.0.1:6379/0"
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/1" #返回结果存储
CELERY_TASK_SERIALIZER='json' #任务序列化方式
CELERY_RESULT_SERIALIZER='json' #任务执行结果序列化方式
CELERY_ACCEPT_CONTENT=['json'] #指定任务接受的内容类型(序列化)
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24 #任务过期时间
CELERYD_CONCURRENCY = 10 #任务并发数
# CELERYD_MAX_TASKS_PER_CHILD = 1000 #每个worker执行多少个任务后会销毁

# CELERY_QUEUES = (
#     Queue("default",Exchange("default"),routing_key="default"),
#     Queue("for_task_A",Exchange("for_task_A"),routing_key="task_a"),
#     Queue("for_task_B",Exchange("for_task_B"),routing_key="task_b")
#     )
  
# CELERY_ROUTES = {
#     'project_app.tasks.taskA':{"queue":"for_task_A","routing_key":"task_a"},
#     'project_app.tasks.taskB':{"queue":"for_task_B","routing_key":"task_b"},
#     'project_app.tasks.test':{"queue":"for_task_A","routing_key":"task_a"}
# }
CELERY_TIMEZONE='Asia/Shanghai'