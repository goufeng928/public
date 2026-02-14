# 文章_Linux运维_Bash脚本_编译安装Wine-9.0(64bit)_GF_2023-03-19

Bash (Bourne Again Shell) 是一个解释器，负责处理 Unix 系统命令行上的命令。它是由 Brian Fox 编写的免费软件，并于 1989 年发布的免费软件，作为 Sh (Bourne Shell) 的替代品。

您可以在 Linux 和 MacOS 机器上使用 Bash，甚至可以通过适用于 Linux 的 Windows 子系统在 Windows 10 机器上使用。

## 使用方法

* 下载源码包:

wine-9.0.tar.xz
  
* 放于指定路径:

这里 Bash Shell 脚本的全局变量 STORAGE 指定的存放源码包的路径 ==/home/goufeng== 可进行修改。
  
* 执行 Bash Shell 脚本:

输入 ==/[路径名]/[脚本名].sh== 即可进行自动编译部署，过程中提示输入 **(y/n)** 输入 **y** 则进行下一步，这样分阶段确认的原因是为了确保能够看到上一个源码编译结果中可能的错误和提示。

## 完整脚本

```shell
#! /bin/bash
# Create By GF 2024-02-19 10:11

# --------------------------------------------------
# Install First: 
# * GNU-Tools (Contains: pkg-config, m4, autoconf, automake, libtool, gettext, flex, bison, libiconv, make)
# * libX11

# -------------------- Wine-9.0 --------------------
# Need File: wine-9.0.tar.xz

# ##################################################
# Recommended Optional Installation
# * GnuTLS-3.7.0 (GnuTLS是一个安全的通信库, 实现 SSL, TLS 和 DTLS 协议及其周围的技术。它提供了用于访问安全通信协议的简单 C语言 应用程序编程接口 (API), 以及用于解析和编写 X.509, PKCS 和其他所需结构的API。)
# * Mesa-23.3.6 (OpenGL) (英语: Open Graphics Library, 译名: 开放图形库或者 "开放式图形库") 是用于渲染 2D, 3D 矢量图形的跨语言, 跨平台的应用程序编程接口 (API)。这个接口由近 350 个不同的函数调用组成, 用来绘制从简单的图形到比较复杂的三维景象。)
# * Wayland-1.22.0 (Wayland 协议定义了图形服务器和客户端之间的通信接口，包括窗口管理、输入事件、渲染等功能。Wayland 是 X11 的现代替代品, 并提供更简洁、高效的图形显示机制。Wayland 项目由红帽开发人员于 2008 年启动。)

# ##################################################
STORAGE=/home/goufeng

# ############################################# Wine-9.0 #############################################

# Function: 编译安装(Compile Install) wine-9.0-64bit
# ##################################################
function compile_install_wine_9_0_64bit() {

    if [[ ! -d "/opt/wine-9.0" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( wine-9.0 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar xvJf $STORAGE/wine-9.0.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # * Problem: configure: error: Cannot build a 32-bit program, you need to install 32-bit development libraries.
        #   - Solve: Configure Add --enable-wine64
        cd $STORAGE/wine-9.0 && ./configure --prefix=/opt/wine-9.0 \
                                            --enable-win64 && \
                                            STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/wine-9.0 && return 0
    else
    
        echo "[Caution] Path: ( /opt/wine-9.0 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

function main() {

    # ----------- Compilation Environment ----------
    # Support: libxcursor 需要引入 X11 的 include 头文件。
    # Support: libxi 需要引入 X11 的 include 头文件。
    # Support: libXxf86vm 需要引入 X11 的 include 头文件。
    # Support: libxrandr 需要引入 X11 的 include 头文件。
    # Support: libxfixes 需要引入 X11 的 include 头文件。
    export C_INCLUDE_PATH=/opt/sandbox-X11/include
    export CPLUS_INCLUDE_PATH=/opt/sandbox-X11/include
    # ..............................................
    # 编译 Wine 9.0 需要引入 X11 的 lib 库文件。
    # Support: OpenGL 需要引入 Mesa 的 lib 库文件。
    export LIBRARY_PATH=/opt/sandbox-X11/lib:/opt/mesa-23.3.6/lib
    export LD_LIBRARY_PATH=/opt/sandbox-X11/lib:/opt/mesa-23.3.6/lib
    # ..............................................
    # 编译 Wine 9.0 需要引入 FreeType 的安装配置信息(PKG Configure)。
    export PKG_CONFIG_PATH=/opt/lib/pkgconfig

    # ------------------ Wine-9.0 ------------------
    compile_install_wine_9_0_64bit
}

main
```

## 总结

以上就是关于 Linux运维 Bash脚本 编译安装Wine-9.0(64bit) 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
