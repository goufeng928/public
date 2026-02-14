# 文章_Linux运维_CentOS7中关闭SELinux的方法_GF_2024-02-07

SELinux (Security-Enhanced Linux) 是美国国家安全局 (NSA) 对于强制访问控制的实现，是 Linux 历史上最杰出的新安全子系统。

NSA 是在 Linux 社区的帮助下开发了一种访问控制体系，在这种访问控制体系的限制下，进程只能访问那些在他的任务中所需要文件。

SELinux 默认安装在 Fedora 和 Red Hat Enterprise Linux 上，也可以作为其他发行版上容易安装的包得到。

## CentOS 7 中临时关闭 SELinux

临时关闭 SELinux:

```shell
setenforce 0
```

查看 SELinux 状态:

```shell
getenforce
```

## CentOS 7 中永久关闭 SELinux

方法 1 直接通过命令关闭 SELinux:

```shell
sed -ri 's/SELINUX=enforcing/SELINUX=disabled/'  /etc/selinux/config
```

方法 2 修改配置文件:

```shell
vim /etc/selinux/config

# 将 `SELINUX=enforcing` 修改为 `SELINUX=disabled`
```

reboot 或 init 6 重启 Linux 服务器让以上配置永久生效。

如果不想现在重启服务器，也可以先临时关闭 SELinux，等到下次重启服务器，SELinux 就可以永久关闭了。

## 总结

以上就是关于 Linux运维 CentOS7中关闭SELinux的方法的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
