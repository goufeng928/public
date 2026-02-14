# 文章_Linux运维_Bash脚本_编译安装X11_GF_2024-02-19

Bash (Bourne Again Shell) 是一个解释器，负责处理 Unix 系统命令行上的命令。它是由 Brian Fox 编写的免费软件，并于 1989 年发布的免费软件，作为 Sh (Bourne Shell) 的替代品。

您可以在 Linux 和 MacOS 机器上使用 Bash，甚至可以通过适用于 Linux 的 Windows 子系统在 Windows 10 机器上使用。

## 使用方法

* 下载源码包:

xproto-7.0.31.tar.gz

xtrans_1.4.0.orig.tar.gz

kbproto-1.0.7.tar.gz

inputproto-2.3.2.tar.gz

xcb-proto-1.14.tar.xz

libXau-1.0.9.tar.gz

libxcb_1.14.orig.tar.gz

xextproto-7.3.0.tar.bz2

libX11-1.6.10.tar.gz

util-macros-1.19.2.tar.bz2

renderproto-0.11.1.tar.gz

libXrender-0.9.10.tar.gz

libXext-1.3.4.tar.gz
  
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

# ------------------ X11 - libX11 ------------------
# Need File: xproto-7.0.31.tar.gz
# Need File: xtrans_1.4.0.orig.tar.gz
# Need File: kbproto-1.0.7.tar.gz
# Need File: inputproto-2.3.2.tar.gz
# Need File: xcb-proto-1.14.tar.xz
# Need File: libXau-1.0.9.tar.gz
# Need File: libxcb_1.14.orig.tar.gz
# Need File: xextproto-7.3.0.tar.bz2
# Need File: libX11-1.6.10.tar.gz
# ---------------- X11 - libXrender ----------------
# Need File: util-macros-1.19.2.tar.bz2
# Need File: renderproto-0.11.1.tar.gz
# Need File: libXrender-0.9.10.tar.gz
# ----------------- X11 - libXext ------------------
# Need File: libXext-1.3.4.tar.gz

# ##################################################
STORAGE=/home/goufeng

# ########################################### X11 - libX11 ###########################################

# Function: 编译安装(Compile Install) xproto-7.0.31
# ##################################################
function compile_install_xproto_7_0_31() {

    if [[ ! -d "/opt/xproto-7.0.31" ]]; then

        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( xproto-7.0.31 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar zxvf $STORAGE/xproto-7.0.31.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/xproto-7.0.31 && ./configure --prefix=/opt/xproto-7.0.31 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # rsync -av /opt/xproto-7.0.31/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/xproto-7.0.31/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/xproto-7.0.31/lib/pkgconfig/xproto.pc /opt/lib/pkgconfig/
            # ......................................
            # Synchronize to sandbox.
            rsync -av /opt/xproto-7.0.31/ /opt/sandbox-X11/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/xproto-7.0.31 && return 0
    else
    
        echo "[Caution] Path: ( /opt/xproto-7.0.31 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) xtrans-1.4.0
# ##################################################
function compile_install_xtrans_1_4_0() {

    if [[ ! -d "/opt/xtrans-1.4.0" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( xtrans-1.4.0 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar zxvf $STORAGE/xtrans_1.4.0.orig.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/xtrans-1.4.0 && ./configure --prefix=/opt/xtrans-1.4.0 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # rsync -av /opt/xtrans-1.4.0/include/ /usr/local/include/
            # ......................................
            cp -f /opt/xtrans-1.4.0/share/pkgconfig/xtrans.pc /opt/lib/pkgconfig/
            # ......................................
            # Synchronize to sandbox.
            rsync -av /opt/xtrans-1.4.0/ /opt/sandbox-X11/
        fi
            
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/xtrans-1.4.0 && return 0
    else
    
        echo "[Caution] Path: ( /opt/xtrans-1.4.0 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) kbproto-1.0.7
# ##################################################
function compile_install_kbproto_1_0_7() {

    if [[ ! -d "/opt/kbproto-1.0.7" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( kbproto-1.0.7 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar zxvf $STORAGE/kbproto-1.0.7.tar.gz && STEP_UNZIPPED=1
         
        # ------------------------------------------
        cd $STORAGE/kbproto-1.0.7 && ./configure --prefix=/opt/kbproto-1.0.7 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # rsync -av /opt/kbproto-1.0.7/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/kbproto-1.0.7/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/kbproto-1.0.7/lib/pkgconfig/kbproto.pc /opt/lib/pkgconfig/
            # ......................................
            # Synchronize to sandbox.
            rsync -av /opt/kbproto-1.0.7/ /opt/sandbox-X11/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/kbproto-1.0.7 && return 0
    else
    
        echo "[Caution] Path: ( /opt/kbproto-1.0.7 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) inputproto-2.3.2
# ##################################################
function compile_install_inputproto_2_3_2() {

    if [[ ! -d "/opt/inputproto-2.3.2" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( inputproto-2.3.2 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar zxvf $STORAGE/inputproto-2.3.2.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/inputproto-2.3.2 && ./configure --prefix=/opt/inputproto-2.3.2 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # rsync -av /opt/inputproto-2.3.2/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/inputproto-2.3.2/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/inputproto-2.3.2/lib/pkgconfig/inputproto.pc /opt/lib/pkgconfig/
            # ......................................
            # Synchronize to sandbox.
            rsync -av /opt/inputproto-2.3.2/ /opt/sandbox-X11/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/inputproto-2.3.2 && return 0
    else
    
        echo "[Caution] Path: ( /opt/inputproto-2.3.2 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) xcb-proto-1.14
# ##################################################
function compile_install_xcb_proto_1_14() {

    if [[ ! -d "/opt/xcb-proto-1.14" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( xcb-proto-1.14 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar xvJf $STORAGE/xcb-proto-1.14.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/xcb-proto-1.14 && ./configure --prefix=/opt/xcb-proto-1.14 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # rsync -av /opt/xcb-proto-1.14/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/xcb-proto-1.14/lib/pkgconfig/xcb-proto.pc /opt/lib/pkgconfig/
            # ......................................
            # Synchronize to sandbox.
            rsync -av /opt/xcb-proto-1.14/ /opt/sandbox-X11/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/xcb-proto-1.14 && return 0
    else
    
        echo "[Caution] Path: ( /opt/xcb-proto-1.14 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) libXau-1.0.9
# ##################################################
function compile_install_libXau_1_0_9() {

    if [[ ! -d "/opt/libXau-1.0.9" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( libXau-1.0.9 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar zxvf $STORAGE/libXau-1.0.9.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/libXau-1.0.9 && ./configure --prefix=/opt/libXau-1.0.9 \
                                                PKG_CONFIG_PATH="/opt/lib/pkgconfig" && \
                                                STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # rsync -av /opt/libXau-1.0.9/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/libXau-1.0.9/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/libXau-1.0.9/lib/pkgconfig/xau.pc /opt/lib/pkgconfig/
            # ......................................
            # Synchronize to sandbox.
            rsync -av /opt/libXau-1.0.9/ /opt/sandbox-X11/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/libXau-1.0.9 && return 0
    else
    
        echo "[Caution] Path: ( /opt/libXau-1.0.9 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) libxcb-1.14
# ##################################################
function compile_install_libxcb_1_14() {

    if [[ ! -d "/opt/libxcb-1.14" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( libxcb-1.14 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar zxvf $STORAGE/libxcb_1.14.orig.tar.gz && STEP_UNZIPPED=1
         
        # ------------------------------------------
        cd $STORAGE/libxcb-1.14 && ./configure --prefix=/opt/libxcb-1.14 \
                                                 PKG_CONFIG_PATH="/opt/lib/pkgconfig" && \
                                                 STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # rsync -av /opt/libxcb-1.14/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/libxcb-1.14/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/libxcb-1.14/lib/pkgconfig/*.pc /opt/lib/pkgconfig/
            # ......................................
            # Synchronize to sandbox.
            rsync -av /opt/libxcb-1.14/ /opt/sandbox-X11/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/libxcb-1.14 && return 0
    else
    
        echo "[Caution] Path: ( /opt/libxcb-1.14 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) xextproto-7.3.0
# ##################################################
function compile_install_xextproto_7_3_0() {

    if [[ ! -d "/opt/xextproto-7.3.0" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( xextproto-7.3.0 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -jxvf $STORAGE/xextproto-7.3.0.tar.bz2 && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/xextproto-7.3.0 && ./configure --prefix=/opt/xextproto-7.3.0 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # rsync -av /opt/xextproto-7.3.0/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/xextproto-7.3.0/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/xextproto-7.3.0/lib/pkgconfig/xextproto.pc /opt/lib/pkgconfig/
            # ......................................
            # Synchronize to sandbox.
            rsync -av /opt/xextproto-7.3.0/ /opt/sandbox-X11/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/xextproto-7.3.0 && return 0
    else
    
        echo "[Caution] Path: ( /opt/xextproto-7.3.0 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 交叉编译安装(Compile Install) libX11-1.6.10
# ##################################################
function compile_install_libX11_1_6_10() {

    if [[ ! -d "/opt/libX11-1.6.10" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( libX11-1.6.10 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar zxvf $STORAGE/libX11-1.6.10.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # * Problem: configure: error: /X11 doesn't exist or isn't a directory
        #   - Solve: sudo mkdir /X11
        # ..........................................
        # * Problem: configure: error: Cannot find keysymdef.h
        #   - Solve: Installed "xproto" and Add --with-keysymdefdir=/opt/xproto-7.0.31/include/X11
        cd $STORAGE/libX11-1.6.10 && ./configure --prefix=/opt/libX11-1.6.10 \
                                                 --with-keysymdefdir=/opt/xproto-7.0.31/include/X11 \
                                                 PKG_CONFIG_PATH="/opt/lib/pkgconfig" && \
                                                 STEP_CONFIGURED=1

        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # rsync -av /opt/libX11-1.6.10/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/libX11-1.6.10/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/libX11-1.6.10/lib/pkgconfig/x11.pc     /opt/lib/pkgconfig/
            cp -f /opt/libX11-1.6.10/lib/pkgconfig/x11-xcb.pc /opt/lib/pkgconfig/
            # ......................................
            # Synchronize to sandbox.
            rsync -av /opt/libX11-1.6.10/ /opt/sandbox-X11/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/libX11-1.6.10 && return 0
    else
    
        echo "[Caution] Path: ( /opt/libX11-1.6.10 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ######################################### X11 - libXrender #########################################

# Function: 交叉编译安装(Compile Install) util-macros-1.19.2
# ##################################################
function compile_install_util_macros_1_19_2() {

    if [[ ! -d "/opt/util-macros-1.19.2" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( util-macros-1.19.2 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -jxvf $STORAGE/util-macros-1.19.2.tar.bz2  && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/util-macros-1.19.2 && ./configure --prefix=/opt/util-macros-1.19.2 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            cp /opt/util-macros-1.19.2/share/pkgconfig/xorg-macros.pc /opt/lib/pkgconfig/
            # ......................................
            # Synchronize to sandbox.
            rsync -av /opt/util-macros-1.19.2/ /opt/sandbox-X11/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/util-macros-1.19.2 && return 0
    else
    
        echo "[Caution] Path: ( /opt/util-macros-1.19.2 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 交叉编译安装(Compile Install) renderproto-0.11.1
# ##################################################
function compile_install_renderproto_0_11_1() {

    if [[ ! -d "/opt/renderproto-0.11.1" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( renderproto-0.11.1 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/renderproto-0.11.1.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/renderproto-0.11.1 && ./configure --prefix=/opt/renderproto-0.11.1 \
                                                      PKG_CONFIG_PATH="/opt/lib/pkgconfig" && \
                                                      STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # rsync -av /opt/renderproto-0.11.1/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/renderproto-0.11.1/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/renderproto-0.11.1/lib/pkgconfig/renderproto.pc /opt/lib/pkgconfig/
            # ......................................
            # Synchronize to sandbox.
            rsync -av /opt/renderproto-0.11.1/ /opt/sandbox-X11/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/renderproto-0.11.1 && return 0
    else
    
        echo "[Caution] Path: ( /opt/renderproto-0.11.1 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 交叉编译安装(Compile Install) libXrender-0.9.10
# ##################################################
function compile_install_libXrender_0_9_10() {

    if [[ ! -d "/opt/libXrender-0.9.10" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( libXrender-0.9.10 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/libXrender-0.9.10.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/libXrender-0.9.10 && ./configure --prefix=/opt/libXrender-0.9.10 \
                                                     PKG_CONFIG_PATH="/opt/lib/pkgconfig" && \
                                                     STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # rsync -av /opt/libXrender-0.9.10/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/libXrender-0.9.10/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/libXrender-0.9.10/lib/pkgconfig/xrender.pc /opt/lib/pkgconfig/
            # ......................................
            # Synchronize to sandbox.
            rsync -av /opt/libXrender-0.9.10/ /opt/sandbox-X11/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/libXrender-0.9.10 && return 0
    else
    
        echo "[Caution] Path: ( /opt/libXrender-0.9.10 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ########################################## X11 - libXext ###########################################

# Function: 编译安装(Compile Install) libXext-1.3.4
# ##################################################
function compile_install_libXext_1_3_4() {

    # Require: "xproto >= 7.0.13"
    # Require: "x11 >= 1.6"
    # Require: "xextproto >= 7.1.99"

    if [[ ! -d "/opt/libXext-1.3.4" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( libXext-1.3.4 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/libXext-1.3.4.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/libXext-1.3.4 && ./configure --prefix=/opt/libXext-1.3.4 \
                                                 PKG_CONFIG_PATH="/opt/lib/pkgconfig" && \
                                                 STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # rsync -av /opt/libXext-1.3.4/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/libXext-1.3.4/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/libXext-1.3.4/lib/pkgconfig/xext.pc /opt/lib/pkgconfig/
            # ......................................
            # Synchronize to sandbox.
            rsync -av /opt/libXext-1.3.4/ /opt/sandbox-X11/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/libXext-1.3.4 && return 0
    else
    
        echo "[Caution] Path: ( /opt/libXext-1.3.4 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

function main() {

    # ---------------- X11 - libX11 ----------------
    compile_install_xproto_7_0_31
    compile_install_xtrans_1_4_0
    compile_install_kbproto_1_0_7
    compile_install_inputproto_2_3_2
    compile_install_xcb_proto_1_14
    compile_install_libXau_1_0_9
    compile_install_libxcb_1_14
    compile_install_xextproto_7_3_0
    compile_install_libX11_1_6_10
    # -------------- X11 - libXrender --------------
    compile_install_util_macros_1_19_2
    compile_install_renderproto_0_11_1
    compile_install_libXrender_0_9_10
    # --------------- X11 - libXext ----------------
    compile_install_libXext_1_3_4
}

main
```

## 总结

以上就是关于 Linux运维 Bash脚本 编译安装X11 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
