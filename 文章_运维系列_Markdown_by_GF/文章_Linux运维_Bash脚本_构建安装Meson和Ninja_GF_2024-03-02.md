# 文章_Linux运维_Bash脚本_构建安装Meson和Ninja_GF_2024-03-02

Bash (Bourne Again Shell) 是一个解释器，负责处理 Unix 系统命令行上的命令。它是由 Brian Fox 编写的免费软件，并于 1989 年发布的免费软件，作为 Sh (Bourne Shell) 的替代品。

您可以在 Linux 和 MacOS 机器上使用 Bash，甚至可以通过适用于 Linux 的 Windows 子系统在 Windows 10 机器上使用。

## 使用方法

* 下载源码包:

meson-1.0.1.tar.gz

re2c-3.1.tar.gz

ninja-1.11.1.tar.gz
  
* 放于指定路径:

这里 Bash Shell 脚本的全局变量 STORAGE 指定的存放源码包的路径 ==/home/goufeng== 可进行修改。
  
* 执行 Bash Shell 脚本:

输入 ==/[路径名]/[脚本名].sh== 即可进行自动编译部署，过程中提示输入 **(y/n)** 输入 **y** 则进行下一步，这样分阶段确认的原因是为了确保能够看到上一个源码编译结果中可能的错误和提示。

## 完整脚本

```shell
#! /bin/bash
# Create By GF 2024-02-20 21:42

# --------------------------------------------------
# Install First:
# * GNU-Tools (Contains: pkg-config, m4, autoconf, automake, libtool, gettext, flex, bison, libiconv, make)

# ------------------ Meson - 1.0.1 -----------------
# Need File: meson-1.0.1.tar.gz
# ---------- Ninja - 1.11.1 - configure.py ---------
# Need File: re2c-3.1.tar.gz
# Need File: ninja-1.11.1.tar.gz

# ##################################################
# Recommended Pairing (Mate):
# * Meson-1.0.1 & Ninja-1.11.1

# ##################################################
STORAGE=/home/goufeng

# ########################################### Meson - 1.0.1 ##########################################

# Function: 构建安装(Build Install) Meson-1.0.1 (by Python3)
# ##################################################
function Build_Install_Meson_1_0_1_by_Python3() {

    if [[ ! -f "/usr/local/bin/meson" ]]; then
    
        # Meson 工具一般和 Ninja 工具一起使用。
        # Meson 可以使用 Python 的 Pip 工具安装: pip install --user meson
        # Meson 可以从源码进行构建安装: python3 setup.py build 以及 python3 setup.py install
        # Ninja 可以使用 Python 的 Pip 工具安装: pip install --user ninja
        # Ninja 可以从源码进行构建安装: python3 ./configure.py --bootstrap (需要下载含有 configure.py 的源码包)
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( meson-1.0.1 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/meson-1.0.1.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/meson-1.0.1 && python3 setup.py build && STEP_BUILDED=1
        
        # ------------------------------------------
        cd $STORAGE/meson-1.0.1 && python3 setup.py install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            ln -sf /opt/Python-3.8.0/bin/meson /usr/local/bin/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/meson-1.0.1 && return 0
    else
    
        echo "[Caution] Bin: ( /usr/local/bin/meson ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ################################### Ninja - 1.11.1 - configure.py ##################################

# Function: 编译安装(Compile Install) re2c-3.1
# ##################################################
function Compile_Install_re2c_3_1() {

    if [[ ! -f "/usr/local/bin/re2c" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_AUTOGEN=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( re2c-3.1 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/re2c-3.1.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # * Problem: aclocal: warning: couldn't open directory 'm4': No such file or directory
        #   - Solve: 只是由于文件夹下没有 m4 文件夹导致, 只需要在当前文件夹下创建一个 m4 文件夹即可 (mkdir m4)。
        # ..........................................
        # * Problem: Makefile.am:477: error: Libtool library used but 'LIBTOOL' is undefined
        #            Makefile.am:477:   The usual way to define 'LIBTOOL' is to add 'LT_INIT'
        #            Makefile.am:477:   to 'configure.ac' and run 'aclocal' and 'autoconf' again.
        #            Makefile.am:477:   If 'LT_INIT' is in 'configure.ac', make sure
        #            Makefile.am:477:   its definition is in aclocal's search path.
        #            autoreconf: automake failed with exit status: 1
        #   - Solve: 原因是 automake 和 libtool 没有安装在同一目录中, 导致 aclocal 在路径中找不到 .m4 文件。
        #            解决方法 (1):
        #                1. 执行 aclocal --print-ac-dir 查看 aclocal 的路径, 例如显示 /opt/automake-1.15/share/aclocal
        #                2. 将 libtool 的 share/aclocal 目录中的 .m4 文件复制到 /opt/automake-1.15/share/aclocal (cp /opt/libtool-2.4.6/share/aclocal/*.m4 /opt/automake-1.15/share/aclocal/)
        #                3. 再次执行 autoreconf, 问题解决。
        #            解决方法 (2):
        #                1. 确保二进制 bin 文件: "aclocal" (包含在 automake 中) 和 "libtoolize" (包含在 libtool 中) 在可找到 PATH 中 (最好是同一路径下)
        #                2. 先执行 libtoolize, 会在当前目录自动生成要用到的 .m4 文件, 再执行 autoreconf, 问题解决。
        cd $STORAGE/re2c-3.1 && ./autogen.sh && STEP_AUTOGEN=1
        
        # ------------------------------------------
        cd $STORAGE/re2c-3.1 && ./configure --prefix=/opt/re2c-3.1 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            ln -sf /opt/re2c-3.1/bin/re2c    /usr/local/bin/
            ln -sf /opt/re2c-3.1/bin/re2go   /usr/local/bin/
            ln -sf /opt/re2c-3.1/bin/re2rust /usr/local/bin/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/re2c-3.1 && return 0
    else
    
        echo "[Caution] Bin: ( /usr/local/bin/re2c ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 构建安装(Build Install) Ninja-1.11.1-by-Py-Configure (by Python3)
# ##################################################
function Build_Install_Ninja_1_11_1_by_Py_Configure_by_Python3() {

    if [[ ! -f "/usr/local/bin/ninja" ]]; then
    
        # Ninja 工具一般配合 Meson 工具使用。
        # Meson 可以使用 Python 的 Pip 工具安装: pip install --user meson
        # Meson 可以从源码进行构建安装: python3 setup.py build 以及 python3 setup.py install
        # Ninja 可以使用 Python 的 Pip 工具安装: pip install --user ninja
        # Ninja 可以从源码进行构建安装: python3 ./configure.py --bootstrap (需要下载含有 configure.py 的源码包)
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( ninja-1.11.1 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar zxvf $STORAGE/ninja-1.11.1.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # * Problem: warning: A compatible version of re2c (>= 0.11.3) was not found; changes to src/*.in.cc will not affect your build.
        #   - Solve: Install re2c.
        # ..........................................
        # * Caution: 构建完成后, 构建目录下将生成 ninja 二进制可执行文件。
        cd $STORAGE/ninja-1.11.1 && python3 ./configure.py --bootstrap && STEP_BUILDED=1
        
        # ------------------------------------------
        # * Caution: 安装 Ninja, 其实就是让系统在需要的时候能找到 Ninja 这个二进制文件并运行。
        if [[ $STEP_BUILDED == 1 ]]; then
            cp $STORAGE/ninja-1.11.1/ninja /usr/local/bin/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/ninja-1.11.1 && return 0
    else
    
        echo "[Caution] Bin: ( /usr/local/bin/ninja ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

function main() {

    # --------------- Meson - 1.0.1 ----------------
    Build_Install_Meson_1_0_1_by_Python3
    # -------- Ninja - 1.11.1 - configure.py -------
    Compile_Install_re2c_3_1
    Build_Install_Ninja_1_11_1_by_Py_Configure_by_Python3
}

main
```

## 总结

以上就是关于 Linux运维 Bash脚本 构建安装Meson和Ninja 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
