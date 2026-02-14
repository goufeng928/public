# 文章_Linux运维_CentOS7中查看_添加_删除firewall端口_GF_2024-02-07

firewalld (Dynamic Firewall Manager of Linux systems，Linux 系统的动态防火墙管理器) 服务是默认的防火墙配置管理工具，它拥有基于 CLI (命令行界面) 和基于 GUI (图形用户界面) 的两种管理方式。

相较于传统的防火墙管理配置工具，firewalld 支持动态更新技术并加入了区域 (zone) 的概念。简单来说，区域就是 firewalld 预先准备了几套防火墙策略集合 (策略模板)，用户可以根据生产场景的不同而选择合适的策略集合，从而实现防火墙策略之间的快速切换。

过滤规则 (执行动作):

* accept (接受)

* drop (丢弃)

* reject (拒绝)

firewalld 配置文件存放目录为 ==/etc/firewalld==

## CentOS 7 中查看已开放的端口

```shell
firewall-cmd --list-ports
```

## CentOS 7 中查询指定端口是否开放 (以 3306 端口为例)

```shell
firewall-cmd --query-port=3306/tcp
```

## CentOS 7 中开放指定端口 (--permanent 代表永久生效)

添加 6379 端口并设置为永久生效:

```shell
firewall-cmd --zone=public --add-port=6379/tcp --permanent
```

添加完端口，一定要重启防火墙，配置才会生效:

```shell
firewall-cmd --reload
```

## CentOS 7 中删除指定端口

删除 13306 端口:

```shell
firewall-cmd --zone=public --remove-port=13306/tcp --permanent
```

删除完端口，一定要重启防火墙，配置才会生效:

```shell
firewall-cmd --reload
```

## 总结

以上就是关于 Linux运维 CentOS7中查看_添加_删除firewall端口的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
