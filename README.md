## WEBSCAN 1.0
基于python2.7.13+django+mysql编写 前端使用layui框架
一款常用的web扫描器,主要提供子域名扫描，端口扫描，目录扫描，插件扫描的项目功能。还可单独检测插件等

本项目仅用于测试、学习使用，不得用于其他非法目的

## 截图

![image](https://github.com/ByHuaiNian/webscan/blob/master/install/img/1.png)

![image](https://github.com/ByHuaiNian/webscan/blob/master/install/img/2.png)

![image](https://github.com/ByHuaiNian/webscan/blob/master/install/img/3.png)

![image](https://github.com/ByHuaiNian/webscan/blob/master/install/img/4.png)

![image](https://github.com/ByHuaiNian/webscan/blob/master/install/img/5.png)


## 功能描述

- 扫描端口
扫描IP段时 需要加子网掩码 如192.168.1.0/24 扫描1-255

- 目录扫描
可组合关键字扫描 目录配置在config.py中

- 插件使用
可选择插件单个测试目标 

- 添加项目
可选择扫描子域名或批量扫描目标 同时可扫描常用端口和目录 相关配置可到config.py中修改 也可选择插件进行扫描

* 扫描子域名可选只扫描二级域名 或者选择扫描多级域名(利用小字典递归扫描三，四，五级等子域名)
* 扫描完子域名会对域名进行存活判断，存活的条件是 requests返回200,403,500 或者可以ping通

* 项目扫描子域名的默认线程为60 dict下放了4个子域名字典数量不同可自行修改。
* 默认扫描端口在config.py中 目录则默认调用default.txt 自定义组合关键词也在config.py中修改 端口，目录，插件扫描的默认线程都为5，可自行修改。

* 任务调用使用celery+Redis

## 插件编写
插件调用使用 Pocsuite 框架 详细信息和POC编写规则请参考 https://github.com/knownsec/Pocsuite/

## 参考项目(感谢大佬们的开源项目)
- [Pocsuite](https://github.com/knownsec/Pocsuite)
- [InsectsAwake](https://github.com/jeffzh3ng/InsectsAwake)
- [w11scan](https://github.com/boy-hack/w11scan)
- [ctf-wscan](https://github.com/kingkaki/ctf-wscan)
- [subDomainsBrute](https://github.com/lijiejie/subDomainsBrute)
- [w9scan](https://github.com/boy-hack/w9scan)
