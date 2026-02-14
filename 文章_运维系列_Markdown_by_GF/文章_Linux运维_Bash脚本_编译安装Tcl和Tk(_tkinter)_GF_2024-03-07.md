# 文章_Linux运维_Bash脚本_编译安装Tcl和Tk(_tkinter)_GF_2024-03-07

Bash (Bourne Again Shell) 是一个解释器，负责处理 Unix 系统命令行上的命令。它是由 Brian Fox 编写的免费软件，并于 1989 年发布的免费软件，作为 Sh (Bourne Shell) 的替代品。

您可以在 Linux 和 MacOS 机器上使用 Bash，甚至可以通过适用于 Linux 的 Windows 子系统在 Windows 10 机器上使用。

## 使用方法

* 下载源码包:

tcl8.6.14-src.tar.gz

tk8.6.14-src.tar.gz
  
* 放于指定路径:

这里 Bash Shell 脚本的全局变量 STORAGE 指定的存放源码包的路径 ==/home/goufeng== 可进行修改。
  
* 执行 Bash Shell 脚本:

输入 ==/[路径名]/[脚本名].sh== 即可进行自动编译部署，过程中提示输入 **(y/n)** 输入 **y** 则进行下一步，这样分阶段确认的原因是为了确保能够看到上一个源码编译结果中可能的错误和提示。

## 完整脚本

```shell
#! /bin/bash
# Create By GF 2024-03-07 12:38

# --------------------------------------------------
# Install First: 
# * GNU-Tools (Contains: pkg-config, m4, autoconf, automake, libtool, gettext, flex, bison, libiconv, make)
# * X11

# -------- Tcl/Tk (Python Module: _tkinter) --------
# Need File: tcl8.6.14-src.tar.gz
# Need File: tk8.6.14-src.tar.gz

# ##################################################
STORAGE=/home/goufeng

# ################################# Tcl/Tk (Python Module: _tkinter) #################################

# Function: 编译安装(Compile Install) Tcl-8.6.14
# ##################################################
function Compile_Install_Tcl_8_6_14() {

    # Tcl/Tk 简介:
    # Tcl 是 "工具控制语言 (Tool Command Language)" 的缩写, 其面向对象为 otcl 语言。
    # Tk 是 Tcl "图形工具箱" 的扩展, 它提供各种标准的 GUI 接口项, 以利于迅速进行高级应用程序开发。

    if [[ ! -d "/opt/tcl-8.6.14" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
        
        # ------------------------------------------
        echo "[Confirm] Compile and Install ( tcl-8.6.14 )? (y/n)"
        # ..........................................
        read VERIFY
        # ..........................................
        if [[ $VERIFY != "y" ]]; then exit 1; fi
        
        # ------------------------------------------
        tar -zxvf $STORAGE/tcl8.6.14-src.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/tcl8.6.14/unix && ./configure --prefix=/opt/tcl-8.6.14 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # ln -sf /opt/tcl-8.6.14/bin/sqlite3_analyzer /usr/local/bin/
            # Skip # ln -sf /opt/tcl-8.6.14/bin/tclsh8.6         /usr/local/bin/
            # ......................................
            rsync -av /opt/tcl-8.6.14/include/ /usr/local/include/
            # ......................................
            rsync -av /opt/tcl-8.6.14/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/tcl-8.6.14/lib/pkgconfig/tcl.pc /opt/lib/pkgconfig/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/tcl-8.6.14 && return 0
    else
        echo "[Caution] Path: ( /opt/tcl-8.6.14 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) Tk-8.6.14
# ##################################################
function Compile_Install_Tk_8_6_14() {

    # Tcl/Tk 简介:
    # Tcl 是 "工具控制语言 (Tool Command Language)" 的缩写, 其面向对象为 otcl 语言。
    # Tk 是 Tcl "图形工具箱" 的扩展, 它提供各种标准的 GUI 接口项, 以利于迅速进行高级应用程序开发。

    if [[ ! -d "/opt/tk-8.6.14" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
        
        # ------------------------------------------
        echo "[Confirm] Compile and Install ( tk-8.6.14 )? (y/n)"
        # ..........................................
        read VERIFY
        # ..........................................
        if [[ $VERIFY != "y" ]]; then exit 1; fi
        
        # ------------------------------------------
        tar -zxvf $STORAGE/tk8.6.14-src.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/tk8.6.14/unix && ./configure --prefix=/opt/tk-8.6.14 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # ln -sf /opt/tk-8.6.14/bin/wish8.6 /usr/local/bin/
            # ......................................
            rsync -av /opt/tk-8.6.14/include/ /usr/local/include/
            # ......................................
            rsync -av /opt/tk-8.6.14/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/tk-8.6.14/lib/pkgconfig/tk.pc /opt/lib/pkgconfig/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/tk-8.6.14 && return 0
    else
        echo "[Caution] Path: ( /opt/tk-8.6.14 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

function main() {

    # ----------- Compilation Environment ----------
    # 编译 Tk 时需要引入 X11 开发套件的 lib 库文件。
    export LIBRARY_PATH=/opt/sandbox-X11/lib
    export LD_LIBRARY_PATH=/opt/sandbox-X11/lib

    # ------ Tcl/Tk (Python Module: _tkinter) ------
    Compile_Install_Tcl_8_6_14
    Compile_Install_Tk_8_6_14
}

main
```

## 总结

以上就是关于 Linux运维 Bash脚本 编译安装Tcl和Tk(_tkinter) 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
