# 文章_Unix运维_FreeBSD-13.1临时环境变量设置(bin和include以及lib)_GF_2023-05-23

在 FreeBSD 系统上设置用户环境变量可以通过编辑用户的 Shell配置文件 来实现。

**cshrc 与 csh_profile 的区别**:

* cshrc: 每个脚本执行前都执行一遍这个脚本。

* csh_profile: 根据不同使用者用户名, 会先去其 home 目录读取 /home/[UserName]/.csh_profile, 再读取 /home/[UserName]/.cshrc。

如果只对当前用户有效, 则在当前用户的 home 目录下的 .cshrc 或 .csh_profile 里增加设定临时环境变量的命令代码。

(由于 Unix 系统会先运行 /etc/csh.cshrc 中的命令, 然后运行 /home/[UserName]/.cshrc 中的命令, 将设定临时环境变量的命令代码写入 /home/[UserName]/.cshrc 则相当于每次启动系统都将为当前用户设定临时环境变量)

如果要对所有用户有效, 则在 /etc/csh.cshrc 增加设定临时环境变量的命令代码。

(由于 Unix 系统会先运行 /etc/csh.cshrc 中的命令, 然后运行 /home/[UserName]/.cshrc 中的命令, 将设定临时环境变量的命令代码写入 /etc/csh.cshrc 则相当于每次启动系统都将为所有用户设定临时环境变量)

## 临时设定 PATH (Binary 二进制可执行文件路径) 环境变量

执行以下命令 (以添加 /opt/bin 为例):

```shell
setenv PATH $PATH:/opt/bin
```

## 临时设定 GCC 编译查找头文件 (Include 文件路径) 环境变量

执行以下命令 (以添加 /opt/include 为例):

```shell
setenv C_INCLUDE_PATH /opt/include:$C_INCLUDE_PATH
```

## 临时设定 G++ 编译查找头文件 (Include 文件路径) 环境变量

执行以下命令 (以添加 /opt/include 为例):

```shell
setenv CPLUS_INCLUDE_PATH /opt/include:$CPLUS_INCLUDE_PATH
```

## 临时设定 GCC 编译前查找库文件 (Library 文件路径) 环境变量

GCC 在编译前使用 LIBRARY_PATH 指定的路径搜索包含需要链接到您的程序的 静态库(Static) 和 共享库(Shared) 的目录。

执行以下命令 (以添加 /opt/lib 为例):

```shell
setenv LIBRARY_PATH /opt/lib:$LIBRARY_PATH
```

## 临时设定 GCC 编译后程序查找库文件 (ILibrary 文件路径) 环境变量

GCC 在成功编译和链接后的程序使用 LD_LIBRARY_PATH 指定的路径搜索包含程序需要的 静态库(Static) 和 共享库(Shared) 的目录。

执行以下命令 (以添加 /opt/lib 为例):

```shell
setenv LD_LIBRARY_PATH /opt/lib:$LD_LIBRARY_PATH
```

## 其它

由于 csh 与 bash不同, csh 等号(=) 前后可以有空格, 而 bash 等号(=) 前后不可以有空格。

## 总结

以上就是关于 Unix运维 FreeBSD-13.1临时环境变量设置(bin和include以及lib) 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
