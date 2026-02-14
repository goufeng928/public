# 文章_Linux运维_Bash脚本_构建安装ReadLine-6.2.4(setup.py)_GF_2024-03-07

Bash (Bourne Again Shell) 是一个解释器，负责处理 Unix 系统命令行上的命令。它是由 Brian Fox 编写的免费软件，并于 1989 年发布的免费软件，作为 Sh (Bourne Shell) 的替代品。

您可以在 Linux 和 MacOS 机器上使用 Bash，甚至可以通过适用于 Linux 的 Windows 子系统在 Windows 10 机器上使用。

## 使用方法

* 下载源码包:

readline-6.2.4.tar.gz
  
* 放于指定路径:

这里 Bash Shell 脚本的全局变量 STORAGE 指定的存放源码包的路径 ==/home/goufeng== 可进行修改。
  
* 执行 Bash Shell 脚本:

输入 ==/[路径名]/[脚本名].sh== 即可进行自动编译部署，过程中提示输入 **(y/n)** 输入 **y** 则进行下一步，这样分阶段确认的原因是为了确保能够看到上一个源码编译结果中可能的错误和提示。

## 完整脚本

```shell
#! /bin/bash
# Create By GF 2024-03-07 13:12

# --------------------------------------------------
# Install First:
# * ncurses
# * Python >= 3.x

# -------------------- ReadLine --------------------
# Need File: readline-6.2.4.tar.gz

# ##################################################
STORAGE=/home/goufeng

# ############################################# ReadLine #############################################

# Function: 构建安装(Build Install) ReadLine-6.2.4 (by Python3)
# ##################################################
function Build_Install_ReadLine_6_2_4_by_Python3() {

    # ----------------------------------------------
    # Python 中的 ReadLine 库说明:
    # Python 的 readline 模块是 GNU Readline Library 的一个封装, Readline 软件包是一个提供命令行编辑和历史纪录功能的库集合。
    # ..............................................
    # 如果没有 readline 模块的话, 比如运行 ipython 无法使用 Tab 键自动补全, 无法使用命令历史功能来方便地进行程序的调试。

    # ----------------------------------------------
    # Linux 中的 expr index 说明:
    # 使用 expr index "$string" "$substring" 来判断字符串 $string 中是否包含子字符串 $substring。
    # Use the expr index "$string" and "$substring" to determine whether the string $string contains a substring $substring.
    # ..............................................
    # 如果子字符串存在, 则返回子字符串在原字符串中的位置 (从 1 开始), 否则返回 0。
    # If the substring exists, return the position of the substring in the original string (starting from 1), otherwise return 0.
    
    local EXISTS_LINE=$(pip3 list | grep "readline")
    local EXISTS_NAME=$(expr index "$EXISTS_LINE" "readline")
    local EXISTS_VERSION=$(expr index "$EXISTS_LINE" "6.2.4")

    if [[ $EXISTS_NAME == 0 && $EXISTS_VERSION == 0 ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( readline-6.2.4 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/readline-6.2.4.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # * Problem: /usr/bin/ld: can not find -lncurses
        #   - Solve: 因为 Python 的 readline 依赖于 Linux 的 ncurses 库, 如果没有这个库, 编译 readline 的时候会提示 can not find -lncurses
        cd $STORAGE/readline-6.2.4 && python3 setup.py build && STEP_BUILDED=1
        
        # ------------------------------------------
        cd $STORAGE/readline-6.2.4 && python3 setup.py install && STEP_INSTALLED=1

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/readline-6.2.4 && return 0
    else
    
        echo "[Caution] Python Program: ( readline-6.2.4 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

function main() {

    # ------------------ ReadLine ------------------
    Build_Install_ReadLine_6_2_4_by_Python3
}

main
```

## 总结

以上就是关于 Linux运维 Bash脚本 构建安装ReadLine-6.2.4(setup.py) 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
