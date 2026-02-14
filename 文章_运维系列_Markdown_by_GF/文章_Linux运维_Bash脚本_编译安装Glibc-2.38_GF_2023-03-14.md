# 文章_Linux运维_Bash脚本_编译安装Glibc-2.38_GF_2023-03-14

Bash (Bourne Again Shell) 是一个解释器，负责处理 Unix 系统命令行上的命令。它是由 Brian Fox 编写的免费软件，并于 1989 年发布的免费软件，作为 Sh (Bourne Shell) 的替代品。

您可以在 Linux 和 MacOS 机器上使用 Bash，甚至可以通过适用于 Linux 的 Windows 子系统在 Windows 10 机器上使用。

## 使用方法

* 下载源码包:

gawk-5.2.2.tar.xz

glib-2.78.4.tar.xz
  
* 放于指定路径:

这里 Bash Shell 脚本的全局变量 STORAGE 指定的存放源码包的路径 ==/home/goufeng== 可进行修改。
  
* 执行 Bash Shell 脚本:

输入 ==/[路径名]/[脚本名].sh== 即可进行自动编译部署，过程中提示输入 **(y/n)** 输入 **y** 则进行下一步，这样分阶段确认的原因是为了确保能够看到上一个源码编译结果中可能的错误和提示。

## 完整脚本

```shell
#! /bin/bash
# Create By GF 2024-03-14 18:52

# --------------------------------------------------
# Install First: 
# * GCC

# ------------------- Dependency -------------------
# Need File: gawk-5.2.2.tar.xz
# ------------------ Glibc - 2.38 ------------------
# Need File: glib-2.78.4.tar.xz

# ##################################################
STORAGE=/home/goufeng

# ############################################ Dependency ############################################

# Function: 编译安装(Compile Install) Gawk-5.2.2
# ##################################################
function Compile_Install_Gawk_5_2_2() {

    if [[ ! -d "/opt/gawk-5.2.2" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
        
        # ------------------------------------------
        echo "[Confirm] Compile and Install ( gawk-5.2.2 )? (y/n)"
        # ..........................................
        read VERIFY
        # ..........................................
        if [[ $VERIFY != "y" ]]; then exit 1; fi
        
        # ------------------------------------------
        tar -Jxvf $STORAGE/gawk-5.2.2.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/gawk-5.2.2 && ./configure --prefix=/opt/gawk-5.2.2 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            # Default None .pc (Pkg-Config) File.
            # ......................................
            # Skip # if [[ ! -d "/usr/local/libexec" ]]; then mkdir /usr/local/libexec; fi
            # ......................................
            # Skip # ln -sf /opt/gawk-5.2.2/bin/* /usr/local/bin/
            # ......................................
            # Skip # rsync -av /opt/gawk-5.2.2/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/gawk-5.2.2/lib/ /usr/local/lib/
            # ......................................
            # Skip # rsync -av /opt/gawk-5.2.2/libexec/ /usr/local/libexec/
            # ......................................
            echo "gawk-5.2.2 has been Installed and Completed."
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/gawk-5.2.2 && return 0
    else
        echo "[Caution] Path: ( /opt/gawk-5.2.2 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ########################################### Glibc - 2.38 ###########################################

# Function: 编译安装(Compile Install) Glibc-2.38
# ##################################################
function Compile_Install_Glibc_2_38() {

    # Glib 和 Glibc 区别和联系 (Differences and connections between Glib and Glibc):
    # ..............................................
    # Glib 不是 Glibc, 尽管两者都是基于 (L)GPL 的开源软件。但这一字之差却误之千里, Glibc 是 GNU 实现的一套标准 C 的库函数, 而 Glib 是 GTK+ 的一套函数库。
    # Glib is not Glibc, although both are open-source software based on (L)GPL. But the difference in this word is a thousand miles. Glibc is a set of standard C library functions implemented by GNU, while Glib is a set of function libraries for GTK+.
    # ..............................................
    # 在 linux 平台上, 像其它任何软件一样, Glib 依赖于 Glibc。
    # On the Linux platform, like any other software, Glib relies on Glibc.
    # ..............................................
    # Glib 不是一个学院派的东西, 也不是凭空想出来的, 完全是在开发 GTK+ 的过程中, 慢慢总结和完善的结果。
    # Glib is not an academic thing, nor was it conceived out of thin air. It is entirely the result of gradually summarizing and improving during the development of GTK+.
    # ..............................................
    # 如果你是一个工作 3 年以上的 C语言 程序员, 现在让你讲讲写程序的苦恼, 你可能有很多话要说, 但如果你有时间研究一下 Glib, 你会发现, 很多苦恼已不再成其为苦恼, Glib 里很多东西正是你期望已经久的。
    # If you are a C language programmer who has been working for more than 3 years, now let's talk about the troubles of writing programs. You may have a lot to say, but if you have time to study Glib, you will find that many troubles are no longer just troubles, and many things in Glib are exactly what you have been hoping for.

    if [[ ! -d "/opt/glibc-2.38" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CREATED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
        
        # ------------------------------------------
        echo "[Confirm] Compile and Install ( glibc-2.38 )? (y/n)"
        # ..........................................
        read VERIFY
        # ..........................................
        if [[ $VERIFY != "y" ]]; then exit 1; fi
        
        # ------------------------------------------
        tar -Jxvf $STORAGE/glibc-2.38.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # The GNU C Library Must Configure in a Separate Build Directory.
        # GNU C Library 必须在单独的构建目录中进行配置。
        mkdir $STORAGE/glibc-2.38/build && STEP_CREATED=1
        
        # ------------------------------------------
        cd $STORAGE/glibc-2.38/build && ../configure --prefix=/opt/glibc-2.38 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            # Default None .pc (Pkg-Config) File.
            # ......................................
            # Skip # if [[ ! -d "/usr/local/sbin" ]]; then mkdir /usr/local/sbin; fi
            # Skip # if [[ ! -d "/usr/local/libexec" ]]; then mkdir /usr/local/libexec; fi
            # ......................................
            # Skip # ln -sf /opt/glibc-2.38/bin/* /usr/local/bin/
            # ......................................
            # Skip # ln -sf /opt/glibc-2.38/sbin/* /usr/local/sbin/
            # ......................................
            # Skip # rsync -av /opt/glibc-2.38/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/glibc-2.38/lib/ /usr/local/lib/
            # ......................................
            # Skip # rsync -av /opt/glibc-2.38/libexec/ /usr/local/libexec/
            # ......................................
            echo "glibc-2.38 has been Installed and Completed."
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/glibc-2.38 && return 0
    else
        echo "[Caution] Path: ( /opt/glibc-2.38 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

function main() {

    # ----------- Compilation Environment ----------
    export PATH=$PATH:/opt/gawk-5.2.2/bin

    # ----------------- Dependency -----------------
    Compile_Install_Gawk_5_2_2
    # ---------------- Glibc - 2.38 ----------------
    Compile_Install_Glibc_2_38
}

main
```

## 总结

以上就是关于 Linux运维 Bash脚本 编译安装Glibc-2.38 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
