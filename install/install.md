# 安装
- 测试于windows server 2012

- 先安装mysql和redis及python2.7.13

- 使用pip安装requirements.txt 中的依赖项 mysql-python需要whl文件安装 已放在文件夹中

- 创建数据库webscan 编码为utf-8

- 在/webscan/settings.py中修改mysql数据库配置

- 根目录下运行python manage.py makemigrations  - python manage.py migrate

- 数据库中运行install下的sql文件 plugin_app_db.sql->plugin_db.sql->users_db.sql 默认账户密码 administrator 123456

- config.py中可修改redis连接信息,各种字典路径,扫描线程数等 配置

- 修改celery配置在/celery_config.py中

- 启动redis

- 启动项目 根目录下运行 python manage.py runserver

- 启动celery 根目录下运行 celery -A ws_celery worker -l info

- 访问http://127.0.0.1:8000/
