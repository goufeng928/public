# 文章_Linux运维_CentOS7中使用yum和rpm命令卸载软件或程序_GF_2024-02-07

rpm: 全称是 Red Hat Package Manager (Red Hat 包管理器)。几乎所有的 Linux 发行版本都使用这种形式的软件包管理安装、更新和卸载软件。rpm 有五种基本的操作功能: 安装、卸载、升级、查询和验证。但是 rpm 软件包之间的依赖性问题往往会很繁琐，尤其是软件由多个 rpm 包组成时。可通过 rpm -help 获取使用帮助。

yum: 是一个在 Fedora 和 RedHat 以及 SUSE 中的 Shell 前端软件包管理器。yum 的宗旨是自动化地升级，安装 / 移除 rpm 包，收集 rpm 包的相关信息，检查依赖性并自动提示用户解决。yum 的关键之处是要有可靠的 repository，即 yum 是软件的仓库，它包含 rpm 的 header, header 包括了 rpm 的各种信息，包括描述，功能，提供的文件，依赖性等，正是收集了这些 header 并加以分析，才能自动化地完成余下地任务。(yum 可以自动的处理依赖性关系，并且一次安装所有依赖的软件包，无须繁琐地一次次下载、安装)

## CentOS 7 中 yum 卸载方式

```shell
yum remove Konqueror
```

温馨提示: CentOS 7 KDE 图形界面自带的 Konqueror 软件不能随便卸载，不然会导致系统崩溃，这里只是举个例子。

出现 Complete! 就证明已经卸载完成了。

## CentOS 7 中 rpm 卸载方式

如果是用 rpm 包安装的软件呢，则使用如下命令进行卸载:

```shell
rpm -e [软件包名]
```

## CentOS 7 中 yum 卸载实例

```shell
[centos@ip-172-31-33-40 ~]$ sudo rpm -qa | grep clamd*  # (提示: rpm -qa | grep 列出需要卸载的安装包, 支持通配符)
clamav-filesystem-0.103.6-1.el7.noarch
clamav-update-0.103.6-1.el7.x86_64
clamav-devel-0.103.6-1.el7.x86_64
clamav-data-0.103.6-1.el7.noarch
clamav-lib-0.103.6-1.el7.x86_64
clamav-0.103.6-1.el7.x86_64
[centos@ip-172-31-33-40 ~]$ sudo yum remove clamav*  # (提示: 执行卸载, 同样支持通配符)
Loaded plugins: fastestmirror
Resolving Dependencies
--> Running transaction check
---> Package clamav.x86_64 0:0.103.6-1.el7 will be erased
---> Package clamav-data.noarch 0:0.103.6-1.el7 will be erased
---> Package clamav-devel.x86_64 0:0.103.6-1.el7 will be erased
---> Package clamav-filesystem.noarch 0:0.103.6-1.el7 will be erased
---> Package clamav-lib.x86_64 0:0.103.6-1.el7 will be erased
---> Package clamav-update.x86_64 0:0.103.6-1.el7 will be erased
--> Finished Dependency Resolution

Dependencies Resolved

================================================================================================================================
Package Arch Version Repository Size
================================================================================================================================
Removing:
clamav x86_64 0.103.6-1.el7 @epel 13 M
clamav-data noarch 0.103.6-1.el7 @epel 219 M
clamav-devel x86_64 0.103.6-1.el7 @epel 73 k
clamav-filesystem noarch 0.103.6-1.el7 @epel 26 k
clamav-lib x86_64 0.103.6-1.el7 @epel 2.2 M
clamav-update x86_64 0.103.6-1.el7 @epel 163 M

Transaction Summary
================================================================================================================================
Remove 6 Packages

Installed size: 397 M
Is this ok [y/N]: y      # (提示: 为防止误删除, 不建议在 yum 中加入 -y)
Downloading packages:
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
Erasing : clamav-devel-0.103.6-1.el7.x86_64 1/6
Erasing : clamav-data-0.103.6-1.el7.noarch 2/6
Erasing : clamav-0.103.6-1.el7.x86_64 3/6
Erasing : clamav-lib-0.103.6-1.el7.x86_64 4/6
Erasing : clamav-update-0.103.6-1.el7.x86_64 5/6
Erasing : clamav-filesystem-0.103.6-1.el7.noarch 6/6
Verifying : clamav-update-0.103.6-1.el7.x86_64 1/6
Verifying : clamav-lib-0.103.6-1.el7.x86_64 2/6
Verifying : clamav-filesystem-0.103.6-1.el7.noarch 3/6
Verifying : clamav-devel-0.103.6-1.el7.x86_64 4/6
Verifying : clamav-data-0.103.6-1.el7.noarch 5/6
Verifying : clamav-0.103.6-1.el7.x86_64 6/6

Removed:
clamav.x86_64 0:0.103.6-1.el7 clamav-data.noarch 0:0.103.6-1.el7 clamav-devel.x86_64 0:0.103.6-1.el7
clamav-filesystem.noarch 0:0.103.6-1.el7 clamav-lib.x86_64 0:0.103.6-1.el7 clamav-update.x86_64 0:0.103.6-1.el7

Complete!
```

## 总结

以上就是关于 Linux运维 CentOS7中使用yum和rpm命令卸载软件或程序的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
