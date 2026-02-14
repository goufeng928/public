# 文章_Linux运维_CentOS6设置开机命令行界面或图形界面启动_GF_2024-02-06

CentOS下的 ==/etc/inittab== 中的英文解释：

This file describes how the INIT process should set up  the system in a certain run-level.The inittab file describes which processes are started  at  bootup  and during  normal operation.

通俗的说就是控制Linux启动时的一些程序及级别。

## CentOS 6 的 6 种运行级别

* 0：关机 -------------- runleve0 --- poweroff.target

* 1：单用户 ------------ runleve1 --- rescue.target

* 2：多用户无网络 ------ runleve2 --- multi-user.target

* 3：多用户有网络 ------ runleve3 --- multi-user.target

* 4：保留 -------------- runleve4 --- multi-user.target

* 5：图形界面 ---------- runleve5 --- graphical.target

* 6：关机并重启 -------- runleve6 --- reboot.target

## CentOS 6 设置开机命令行界面或图形界面启动

```shell
vim /etc/inittab

id:5:initdefault: -----> id:3:initdefault:
```

## 总结

以上就是关于 Linux运维 CentOS6设置开机命令行界面或图形界面启动的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
