# 文章_Linux运维_Bash脚本_编译安装Net-Tools-2.10_GF_2024-02-06

Bash (Bourne Again Shell) 是一个解释器，负责处理 Unix 系统命令行上的命令。它是由 Brian Fox 编写的免费软件，并于 1989 年发布的免费软件，作为 Sh (Bourne Shell) 的替代品。

您可以在 Linux 和 MacOS 机器上使用 Bash，甚至可以通过适用于 Linux 的 Windows 子系统在 Windows 10 机器上使用。

## 使用方法

* 下载源码包:

net-tools-2.10.tar.xz
  
* 放于指定路径:

这里 Bash Shell 脚本的全局变量 STORAGE 指定的存放源码包的路径 ==/home/goufeng== 可进行修改。
  
* 执行 Bash Shell 脚本:

输入 ==/[路径名]/[脚本名].sh== 即可进行自动编译部署，过程中提示输入 **(y/n)** 输入 **y** 则进行下一步，这样分阶段确认的原因是为了确保能够看到上一个源码编译结果中可能的错误和提示。

## 完整脚本

```shell
#! /bin/bash
# Create By GF 2023-03-21 17:23

# Need File : net-tools-2.10.tar.xz

STORAGE=/home/goufeng

# Function: 编译安装(Compile Install) net-tools-2.10
# ##################################################
function compile_install_net_tools_2_10() {

    if [[ ! -f "/usr/bin/ifconfig" ]]; then
    
        local verify
    
        read -p "[Confirm] Compile and Install ( net-tools-2.10 )? (y/n)>" verify
        
        if [[ "$verify" != "y" ]]; then exit 1; fi

        tar xvJf $STORAGE/net-tools-2.10.tar.xz && \
	                                               \
        cd $STORAGE/net-tools-2.10              && \
	                                               \
        yes "" | make config                    && \
	                                               \
        make && make install                    && \
	                                               \
        cd $STORAGE                             && \
                                                   \
        rm -rf $STORAGE/net-tools-2.10          && \
                                                   \
        return 0
    else
    
        echo "[Caution] Path: ( /usr/bin/ifconfig ) Already Exists."
        
        return 0
    fi
}

function main() {

    compile_install_net_tools_2_10
}

main
```

## 总结

以上就是关于 Linux运维 Bash脚本 编译安装Net-Tools-2.10 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
