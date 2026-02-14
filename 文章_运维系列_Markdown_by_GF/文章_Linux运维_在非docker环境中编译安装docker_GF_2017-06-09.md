# 文章_Linux运维_在非docker环境中编译安装docker_GF_2017-06-09

最近要修改 docker 的源码做一些开发。

但是 docker 的官网给的编译方式是用 docker 提供的 dockerfile 文件构建一个 docker 容器然后在这个容器里面通过脚本编译 docker。

我们都知道 1.11 以后的 docker 实际上有 docker, dockerd, docker-containerd, runc 几个进程组成。

如果我修改一次就要全部编译一遍多麻烦。所以我觉定自己 go build 出 docker 的几个可执行文件。

## 1. 编译前准备

现在 docker 的代码从 github.com/docker/docker 迁移到了 github.com/moby/moby。

```shell
git clone github.com/moby/moby
```

当然在编译之前还需要安装 go。这个 Golang 官网都有说明, 按照说明安装就好。

## 2. 编译 docker

编译 docker 就是编译 docker client。

这里以 1.13.x 分支为例, 代码在 cmd/docker 下。

在你的 GOPATH 路径下还有一个 docker/docker 的目录你要保持 docker 下的分支和 moby 下的一致。不然在 moby 下 build 会出错。

然后执行 go build。会生成 docker 的 bin 文件。

## 3. 编译 dockerd

编译 dockerd 的时候需要安装许多包。

可以根据错误提示安装需要的包。

例如我是 fedora25。go build 会报 libdevmapper.h 缺少。执行 dnf install device-mapper-devel.x86_6 即可。

## 4. 编译 containerd

Clone 源码:

```shell
git clone github.com/docker/containerd
```

编译 containerd 使用 containerd 的 make file 来编译生成。

编译完以后会生成 containerd-shim, containerd。

具体参考 containerd 的 README。

## 5. 编译生成 runc

runc 是最终启动容器的工具, 可以说容器的核心。

实际上没有 dockerd 也是发送命令到 containerd, 然后 containerd 再启动 containd-shim, 之后 containerd-shim 再调用 runc 来启动容器, 停止容器等容器运行生命周期的各种操作。

其实没有前几个进程, 可以直接发送数据给 runc 启动容器。当然了要符合 oci 的标准。

具体可以参考 runc 项目的 README。

runc 现在在 https://github.com/opencontainers/runc。

docker 变曾经的 libcontainer 贡献出来改了个名字变成 cncf 下的 runc 项目。

runc 编译就 go build 一下。具体看 github 的 README 写的非常详细。

## 6. 完成编译

现在 docker 需要的 5 个 bin 文件全部都编译生成完成。分别是 docker, dockerd, containerd, containerd-shim 和 runc。

编译这些可执行文件主要是为了方便我调试 docker 代码。

后面我会修改 docker, dockerd, containerd 等。从一条 docker run 看数据如何在这几个进程间流动。如何互相调用。

## 总结

以上就是关于 Linux运维 在非docker环境中编译安装docker 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
