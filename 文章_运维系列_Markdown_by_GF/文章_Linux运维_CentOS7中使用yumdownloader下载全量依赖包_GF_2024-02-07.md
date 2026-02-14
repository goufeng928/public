# 文章_Linux运维_CentOS7中使用yumdownloader下载全量依赖包_GF_2024-02-07

在一台可联网的服务器上部署，我们会感觉如鱼得水，使用万能的 vim 可以为所欲为，但是一旦切换到了无网的服务器上，很多服务的部署就会举步维艰，比如说我们要部署一个 nginx，就需要首先安装他的 gcc, pcre, pcre-devel, zlib, zlib-devel, ...... 非常麻烦，有没有一种东西可以像联网服务器的 yum 一样方便呢，直接一条命令就部署该程序，连带安装此程序的依赖呢? 此时 yumdownloader 就来了。

yumdownloader 可以方便的导出 yum 部署的应用的所有依赖。移动到无网环境可以直接一键安装。

## CentOS 7 安装 yum-utils

```shell
yum -y install yum-utils
```

## CentOS 7 下载软件依赖包

```shell
yumdownloader --resolve --destdir=/home/goufeng/temp [软件包名]
```

选项说明:

* **destdir**: 指定 rpm 包下载目录 (不指定时默认为当前目录)。

* **resolve**: 下载依赖的 rpm 包。

## 总结

以上就是关于 Linux运维 CentOS7中使用yumdownloader下载全量依赖包的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
