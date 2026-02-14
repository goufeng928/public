# 文章_Linux运维_Linux临时环境变量设置(bin和include以及lib)_GF_2023-05-22

在 Linxu 系统上设置用户环境变量可以通过编辑用户的 profile 环境变量配置文件或者 .bashrc Shell配置文件来实现。

**bashrc 与 profile 的区别**:

* bashrc: 每个脚本执行前都执行一遍这个脚本。

* profile: 在系统登录后执行 1 次(只执行 1 次), 包括针对所有用户的 /etc/profile 和针对用户的 /home/[UserName]/.profile。

如果只对当前用户有效, 则在当前用户的 home 目录下的 .profile 里增加设定临时环境变量的命令代码。

(由于 Unix 系统启动时, 会先运行 /etc/profile 中的命令, 然后运行 /home/[UserName]/.profile 中的命令, 将设定临时环境变量的命令代码写入 /home/[UserName]/.profile 则相当于每次启动系统都将为当前用户设定临时环境变量)

如果要对所有用户有效, 则在 /etc/profile 增加设定临时环境变量的命令代码。

(由于 Unix 系统启动时, 会先运行 /etc/profile 中的命令, 然后运行 /home/[UserName]/.profile 中的命令, 将设定临时环境变量的命令代码写入 /etc/profile 则相当于每次启动系统都将为所有用户设定临时环境变量)

## 临时设定 PATH (Binary 二进制可执行文件路径) 环境变量

执行以下命令 (以添加 /opt/bin 为例):

```shell
export PATH $PATH:/opt/bin
```

## 临时设定 GCC 编译查找头文件 (Include 文件路径) 环境变量

执行以下命令 (以添加 /opt/include 为例):

```shell
export C_INCLUDE_PATH /opt/include:$C_INCLUDE_PATH
```

## 临时设定 G++ 编译查找头文件 (Include 文件路径) 环境变量

执行以下命令 (以添加 /opt/include 为例):

```shell
export CPLUS_INCLUDE_PATH /opt/include:$CPLUS_INCLUDE_PATH
```

## 临时设定 GCC 编译前查找库文件 (Library 文件路径) 环境变量

GCC 在编译前使用 LIBRARY_PATH 指定的路径搜索包含需要链接到您的程序的 静态库(Static) 和 共享库(Shared) 的目录。

执行以下命令 (以添加 /opt/lib 为例):

```shell
export LIBRARY_PATH /opt/lib:$LIBRARY_PATH
```

## 临时设定 GCC 编译后程序查找库文件 (ILibrary 文件路径) 环境变量

GCC 在成功编译和链接后的程序使用 LD_LIBRARY_PATH 指定的路径搜索包含程序需要的 静态库(Static) 和 共享库(Shared) 的目录。

执行以下命令 (以添加 /opt/lib 为例):

```shell
export LD_LIBRARY_PATH /opt/lib:$LD_LIBRARY_PATH
```

## 其它

当登入系统时候获得一个 Shell 进程时, 其读取环境设定档有三步:

1. 首先读入的是全局环境变量设定档 /etc/profile, 然后根据其内容读取额外的设定的文档, 如 /etc/profile.d 下的所有 .sh 和 /etc/inputrc。

2. 然后根据不同使用者用户名, 去其 home 目录读取 /home/[UserName]/.bash_profile, 如果这读取不了就读取 /home/[UserName]/.bash_login, 这个也读取不了才会读取 /home/[UserName]/.profile 这三个文档设定基本上是一样的, 读取有优先关系。

3. 然后再根据用户名读取 /home/[UserName]/.bashrc。

## 总结

以上就是关于 Linux运维 Linux临时环境变量设置(bin和include以及lib) 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
