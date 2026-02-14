# 文章_Linux运维_Bash脚本_编译安装GetText-0.22.4_GF_2024-02-21

Bash (Bourne Again Shell) 是一个解释器，负责处理 Unix 系统命令行上的命令。它是由 Brian Fox 编写的免费软件，并于 1989 年发布的免费软件，作为 Sh (Bourne Shell) 的替代品。

您可以在 Linux 和 MacOS 机器上使用 Bash，甚至可以通过适用于 Linux 的 Windows 子系统在 Windows 10 机器上使用。

## 使用方法

* 下载源码包:

gettext-0.22.4.tar.xz
  
* 放于指定路径:

这里 Bash Shell 脚本的全局变量 STORAGE 指定的存放源码包的路径 ==/home/goufeng== 可进行修改。
  
* 执行 Bash Shell 脚本:

输入 ==/[路径名]/[脚本名].sh== 即可进行自动编译部署，过程中提示输入 **(y/n)** 输入 **y** 则进行下一步，这样分阶段确认的原因是为了确保能够看到上一个源码编译结果中可能的错误和提示。

## 完整脚本

```shell
#! /bin/bash
# Create By GF 2024-02-21 20:50

# Need File: gettext-0.22.4.tar.xz

# ##################################################
STORAGE=/home/goufeng

# Function: 编译安装(Compile Install) gettext-0.22.4 (for Linux)
# ##################################################
function compile_install_gettext_0_22_4_for_linux() {

    if [[ ! -f "/usr/local/bin/gettext" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( gettext-0.22.4 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar xvJf $STORAGE/gettext-0.22.4.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # Must Be "Shared (--enable-shared)" To Be Called By Other Programs.
        cd $STORAGE/gettext-0.22.4 && ./configure --enabel-shared && ldconfig && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/gettext-0.22.4 && return 0
    else
    
        echo "[Caution] Bin: ( /usr/local/bin/gettext ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

function main() {

    compile_install_gettext_0_22_4_for_linux
}

main
```

## 总结

以上就是关于 Linux运维 Bash脚本 编译安装GetText-0.22.4 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
