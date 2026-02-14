# 文章_Linux运维_Bash脚本_编译安装Python-3.8.0_GF_2024-02-06

Bash (Bourne Again Shell) 是一个解释器，负责处理 Unix 系统命令行上的命令。它是由 Brian Fox 编写的免费软件，并于 1989 年发布的免费软件，作为 Sh (Bourne Shell) 的替代品。

您可以在 Linux 和 MacOS 机器上使用 Bash，甚至可以通过适用于 Linux 的 Windows 子系统在 Windows 10 机器上使用。

## 使用方法

* 下载源码包:

zlib-1.2.13.tar.gz

openssl-1.1.1g.tar.gz

libffi-3.4.4.tar.gz

ncurses-6.4.tar.gz

readline-8.2.tar.gz

Python-3.8.0.tgz
  
* 放于指定路径:

这里 Bash Shell 脚本的全局变量 STORAGE 指定的存放源码包的路径 ==/home/goufeng== 可进行修改。
  
* 执行 Bash Shell 脚本:

输入 ==/[路径名]/[脚本名].sh== 即可进行自动编译部署，过程中提示输入 **(y/n)** 输入 **y** 则进行下一步，这样分阶段确认的原因是为了确保能够看到上一个源码编译结果中可能的错误和提示。

## 完整脚本

```shell
#! /bin/bash
# Create By GF 2023-04-03 16:47

# --------------------------------------------------
# Install First: 
# * None

# ------------------- Dependency -------------------
# Need File: zlib-1.2.13.tar.gz
# Need File: openssl-1.1.1g.tar.gz
# ------------ libffi (Module: _ctypes) ------------
# Need File: libffi-3.4.4.tar.gz
# ---------- ReadLine (Module: readline) -----------
# Need File: ncurses-6.4.tar.gz
# Need File: readline-8.2.tar.gz
# --------------------- Python ---------------------
# Need File: Python-3.8.0.tgz

# ##################################################
STORAGE=/home/goufeng

# ##################################################
# Recommended Optional Installation
# * Tcl/Tk-8.6.14 (Tcl 是 "工具控制语言 (Tool Command Language)" 的缩写, 其面向对象为 otcl 语言。Tk 是 Tcl "图形工具箱" 的扩展, 它提供各种标准的 GUI 接口项, 以利于迅速进行高级应用程序开发。)

# ############################################ Dependency ############################################

# Function: 编译安装(Compile Install) zlib-1.2.13
# ##################################################
function Compile_Install_zlib_1_2_13() {

    if [[ ! -f "/usr/include/zlib.h" && ! -f "/usr/local/include/zlib.h" && ! -d "/opt/zlib-1.2.13" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( zlib-1.2.13 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/zlib-1.2.13.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/zlib-1.2.13 && ./configure --prefix=/opt/zlib-1.2.13 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            rsync -av /opt/zlib-1.2.13/include/ /usr/local/include/
            rsync -av /opt/zlib-1.2.13/lib/     /usr/local/lib/
            # ......................................
            cp /opt/zlib-1.2.13/lib/pkgconfig/zlib.pc /opt/lib/pkgconfig/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/zlib-1.2.13 && return 0
    else
    
        echo "[Caution] Program: ( /usr/include/zlib.h or /usr/local/include/zlib.h or /opt/zlib-1.2.13 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) openssl-1.1.1g
# ##################################################
function Compile_Install_openssl_1_1_1g() {

    if [[ ! -d "/opt/openssl-1.1.1g" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( openssl-1.1.1g )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/openssl-1.1.1g.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/openssl-1.1.1g && ./config --prefix=/opt/openssl-1.1.1g \
                                               --openssldir=/opt/openssl-1.1.1g/ssl \
                                               --shared \
                                               zlib && \
                                               STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            cp -f /opt/openssl-1.1.1g/lib/pkgconfig/libcrypto.pc /opt/lib/pkgconfig/
            cp -f /opt/openssl-1.1.1g/lib/pkgconfig/libssl.pc    /opt/lib/pkgconfig/
            cp -f /opt/openssl-1.1.1g/lib/pkgconfig/openssl.pc   /opt/lib/pkgconfig/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/openssl-1.1.1g && return 0
    else
    
        echo "[Caution] Path: ( /opt/openssl-1.1.1g ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ##################################### libffi (Module: _ctypes) #####################################

# Function: 编译安装(Compile Install) libffi-3.4.4 (for Linux)
# ##################################################
function Compile_Install_libffi_3_4_4_for_Linux() {

    if [[ ! -d "/opt/libffi-3.4.4" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
        
        # ------------------------------------------
        echo "[Confirm] Compile and Install ( libffi-3.4.4 )? (y/n)"
        # ..........................................
        read VERIFY
        # ..........................................
        if [[ $VERIFY != "y" ]]; then exit 1; fi
        
        # ------------------------------------------
        tar -zxvf $STORAGE/libffi-3.4.4.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/libffi-3.4.4 && ./configure --prefix=/opt/libffi-3.4.4 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            rsync -av /opt/libffi-3.4.4/include/ /usr/local/include/
            rsync -av /opt/libffi-3.4.4/lib/     /usr/local/lib/
            # ......................................
            cp -f /opt/libffi-3.4.4/lib/pkgconfig/libffi.pc /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        ldconfig
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/libffi-3.4.4 && return 0
    else
        echo "[Caution] Path: ( /opt/libffi-3.4.4 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ################################### ReadLine (Module: readline) ####################################

# Function: 编译安装(Compile Install) ncurses-6.4
# ##################################################
function Compile_Install_ncurses_6_4() {

    # ncurses (new curses) 是一套编程库，它提供了一系列的函数以便使用者调用它们去生成基于文本的用户界面。
    # ncurses 名字中的n意味着 "new", 因为它是 curses 的自由软件版本。由于 AT&T "臭名昭著" 的版权政策, 人们不得不在后来用 ncurses 去代替它。
    # ncurses 是 GNU 计划的一部分, 但它却是少数几个不使用 GNU GPL 或 LGPL 授权的 GNU 软件之一。
    # 其实我们对 ncurses 本身并不陌生，以下几款大名鼎鼎的软件都用到过 ncurses:
    #     * vim
    #     * emacs
    #     * lynx
    #     * screen
    # 作为嵌入式驱动开发工程师, Linux 内核的配置也离不开 ncurses 库的使用。

    if [[ ! -d "/opt/ncurses-6.4" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
        
        # ------------------------------------------
        echo "[Confirm] Compile and Install ( ncurses-6.4 )? (y/n)"
        # ..........................................
        read VERIFY
        # ..........................................
        if [[ $VERIFY != "y" ]]; then exit 1; fi
        
        # ------------------------------------------
        tar -zxvf $STORAGE/ncurses-6.4.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/ncurses-6.4 && ./configure --prefix=/opt/ncurses-6.4 \
                                               --enable-pc-files \
                                               --enable-shared \
                                               --with-libtool && \
                                               STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/usr/local/lib/terminfo" ]]; then mkdir /usr/local/lib/terminfo; fi
            # ......................................
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # ln -sf /opt/ncurses-6.4/bin/* /usr/local/bin/
            # ......................................
            rsync -av /opt/ncurses-6.4/include/ /usr/local/include/
            # ......................................
            cp -vf /opt/ncurses-6.4/include/ncurses/*.h /usr/local/include/
            # ......................................
            rsync -av /opt/ncurses-6.4/lib/ /usr/local/lib/
            # ......................................
            rsync -av /opt/ncurses-6.4/share/terminfo/ /usr/local/lib/terminfo/
            # ......................................
            cp -vf /opt/ncurses-6.4/lib/pkgconfig/*.pc /opt/lib/pkgconfig/
        fi
        
        # ------------------------------------------
        # Ubuntu Linux Proprietary Command.
        ldconfig
        
        # ------------------------------------------
        # FreeBSD Unix Proprietary Command.
        /etc/rc.d/ldconfig restart
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/ncurses-6.4 && return 0
    else
        echo "[Caution] Path: ( /opt/ncurses-6.4 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) readline-8.2
# ##################################################
function Compile_Install_readline_8_2() {

    # 编译安装 readline 之前, 需要确保 ncurses 已经存在并可调用, 因为 readline can be called when ncurses lib is installed.
    # 所以 ncurses 是 readline 的依赖软, 虽然不安装 ncurses 也能将 readline 编译通过, 但 readline 不能被调用, 没有意义。

    if [[ ! -d "/opt/readline-8.2" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
        
        # ------------------------------------------
        echo "[Confirm] Compile and Install ( readline-8.2 )? (y/n)"
        # ..........................................
        read VERIFY
        # ..........................................
        if [[ $VERIFY != "y" ]]; then exit 1; fi
        
        # ------------------------------------------
        tar -zxvf $STORAGE/readline-8.2.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/readline-8.2 && ./configure --prefix=/opt/readline-8.2 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            rsync -av /opt/readline-8.2/include/ /usr/local/include/
            rsync -av /opt/readline-8.2/lib/     /usr/local/lib/
            # ......................................
            cp -f /opt/readline-8.2/lib/pkgconfig/history.pc  /opt/lib/pkgconfig/
            cp -f /opt/readline-8.2/lib/pkgconfig/readline.pc /opt/lib/pkgconfig/
        fi
        
        # ------------------------------------------
        ldconfig
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/readline-8.2 && return 0
    else
        echo "[Caution] Path: ( /opt/readline-8.2 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ############################################## Python ##############################################

# Function: 编译安装(Compile Install) Python-3.8.0
# ##################################################
function Compile_Install_Python_3_8_0() {

    # ----------------------------------------------
    # * Problem:   File "/usr/local/lib/python3.8/ctypes/__init__.py", line 7, in <module>
    #                from _ctypes import Union, Structure, Array
    #            ModuleNotFoundError: No module named '_ctypes'
    #   - Solve: Python3 中有个内置模块叫 ctypes, 它是 Python3 的外部函数库模块, 它提供兼容 C 语言的数据类型, 并通过它调用 Linux 系统下的共享库 (Shared library)。
    #            There is a built-in module called ctypes in Python3, which is an external function library module of Python3. It provides data types compatible with the C language and calls the shared library on Linux systems through it.
    #            # .................................
    #            此模块需要使用 Linux 系统中外部函数库 (Foreign function library) 的开发链接库 (头文件和链接库)。
    #            This module requires the use of the development link library (header files and link libraries) of the Foreign Function Library in Linux systems.
    #            # .................................
    #            由于在 Linux 系统中没有安装外部函数库 (libffi) 的开发链接库软件包, 所以在 import _ctypes 的时候就会报 ModuleNotFoundError: No module named '_ctypes' 错误。
    #            Due to the lack of a development link library package for the external function library (libffi) installed in the Linux system, a ModuleNotFoundError: No module named '_ctypes' error will be reported when importing _ctypes.
    #            # .................................
    #            安装 libffi 后重新编译 Python3 即可解决这个问题。
    #            After installing libffi, recompile Python3 to solve this problem.
    # ..............................................
    # * Problem: Fatal: ./Include/py_curses.h:36:10: fatal error: curses.h: 没有那个文件或目录
    #                    #include <curses.h>
    #   - Solve: 源码新老版本头文件路径问题。
    #            cp /usr/local/include/ncurses/*.h /usr/local/include/
    # ..............................................
    # * Problem: /home/goufeng/Python-3.8.0/Modules/_cursesmodule.c:3240:35: error: implicit declaration of function ‘setupterm’; did you mean ‘set_term’? [-Werror=implicit-function-declaration]
    #                 if (!initialised_setupterm && setupterm((char *)term, fd, &err) == ERR) {
    #                                               ^~~~~~~~~
    #                                               set_term
    #   - Solve: 源码新老版本函数名称问题。
    #            sed -i "3240s/setupterm\(\(char \*\)term\, fd\, \&err\)/set_term\(\(char \*\)term\, fd\, \&err\)/" ./Python-3.8.0/Modules/_cursesmodule.c
    # ..............................................
    # * Problem: /usr/bin/ld: /usr/local/lib/libncurses.a(read_entry.o): relocation R_X86_64_PC32 against symbol `_nc_user_definable' can not be used when making a shared object; recompile with -fPIC
    #            ChatGPT 对该问题的解释: 你的程序在链接时发现一个库 (libncurses.a) 不是用 -fPIC (Position Independent Code) 编译的。
    #                                    在编译共享库 (shared library) 时, 通常需要确保所有的对象文件和库都使用 -fPIC 选项进行编译。
    #   - Solve: 方法 A. 添加 -fPIC (未奏效)。
    #            编译安装 ncurses 时添加配置参数 ./configure CFLAGS="-fPIC -no-pie" 或者 ./configure --with-build-cflags="-fPIC -no-pie" 选项中, 抑或者添加在 Makefile 中的 CFLAGS 变量中。
    #            ...................................
    #            方法 B. 配置选项 --with-libtool 编译出 .so 文件。
    #            编译安装 ncurses 时添加配置参数 ./configure --with-libtool 即可编译出 .so 文件。
    # ..............................................
    # * Problem: *** WARNING: renaming "_curses" since importing it failed: libncurses.so.6: cannot open shared object file: No such file or directory
    #            *** WARNING: renaming "_curses_panel" since importing it failed: libpanel.so.6: cannot open shared object file: No such file or directory
    #   - Solve: 如果 libncurses.so.6 存在, 则可能是 libncurses.so.6 未加载, 在 Linux 系统中执行 ldconfig 命令。
    
    if [[ ! -d "/opt/Python-3.8.0" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( Python-3.8.0 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/Python-3.8.0.tgz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        if [[ $STEP_UNZIPPED == 1 ]]; then
            sed -i "3240s/setupterm\(\(char \*\)term\, fd\, \&err\)/set_term\(\(char \*\)term\, fd\, \&err\)/" $STORAGE/Python-3.8.0/Modules/_cursesmodule.c
        fi

        # ------------------------------------------
        cd $STORAGE/Python-3.8.0 && ./configure --prefix=/opt/Python-3.8.0 \
                                                --with-openssl=/opt/openssl-1.1.1g && \
                                                STEP_CONFIGURED=1

        # ------------------------------------------
        make && make install && STEP_INSTALLED=1

        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            if [[ -f "/usr/bin/python3" ]]; then mv /usr/bin/python3 /usr/bin/python3.bak; fi
            if [[ -f "/usr/bin/pip3" ]]; then mv /usr/bin/pip3 /usr/bin/pip3.bak; fi
            # ......................................
            if [[ -f "/usr/local/bin/python3" ]]; then mv /usr/bin/local/python3 /usr/bin/local/python3.bak; fi
            if [[ -f "/usr/local/bin/pip3" ]]; then mv /usr/local/bin/pip3 /usr/local/bin/pip3.bak; fi
            # ......................................
            ln -sf /opt/Python-3.8.0/bin/python3 /usr/local/bin/
            ln -sf /opt/Python-3.8.0/bin/pip3    /usr/local/bin/
            # ......................................
            rsync -av /opt/Python-3.8.0/include/ /usr/local/include/
            rsync -av /opt/Python-3.8.0/lib/     /usr/local/lib/
            # ......................................
            cp -f /opt/Python-3.8.0/lib/pkgconfig/python-3.8-embed.pc /opt/lib/pkgconfig/
            cp -f /opt/Python-3.8.0/lib/pkgconfig/python-3.8.pc       /opt/lib/pkgconfig/
            cp -f /opt/Python-3.8.0/lib/pkgconfig/python3-embed.pc    /opt/lib/pkgconfig/
            cp -f /opt/Python-3.8.0/lib/pkgconfig/python3.pc          /opt/lib/pkgconfig/
            
            
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/Python-3.8.0 && return 0
    else
    
        echo "[Caution] Path: ( /opt/Python-3.8.0 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

function main() {

    # ----------------- Dependency -----------------
    Compile_Install_zlib_1_2_13
    Compile_Install_openssl_1_1_1g
    # ---------- libffi (Module: _ctypes) ----------
    Compile_Install_libffi_3_4_4_for_Linux
    # -------- ReadLine (Module: readline) ---------
    Compile_Install_ncurses_6_4
    Compile_Install_readline_8_2
    # ------------------- Python -------------------
    Compile_Install_Python_3_8_0
}

main
```

## 总结

以上就是关于 Linux运维 Bash脚本 编译安装 Python-3.8.0 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
