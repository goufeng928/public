# 文章_Linux运维_Bash脚本_构建安装Neat-VNC-0.7.2_GF_2023-03-09

Bash (Bourne Again Shell) 是一个解释器，负责处理 Unix 系统命令行上的命令。它是由 Brian Fox 编写的免费软件，并于 1989 年发布的免费软件，作为 Sh (Bourne Shell) 的替代品。

您可以在 Linux 和 MacOS 机器上使用 Bash，甚至可以通过适用于 Linux 的 Windows 子系统在 Windows 10 机器上使用。

## 使用方法

* 下载源码包:

aml-0.3.0.tar.gz

neatvnc-0.7.2.tar.gz
  
* 放于指定路径:

这里 Bash Shell 脚本的全局变量 STORAGE 指定的存放源码包的路径 ==/home/goufeng== 可进行修改。
  
* 执行 Bash Shell 脚本:

输入 ==/[路径名]/[脚本名].sh== 即可进行自动编译部署，过程中提示输入 **(y/n)** 输入 **y** 则进行下一步，这样分阶段确认的原因是为了确保能够看到上一个源码编译结果中可能的错误和提示。

## 完整脚本

```shell
#! /bin/bash
# Create By GF 2024-03-09 01:22

# --------------------------------------------------
# Install First: 
# * GNU-Tools (Contains: pkg-config, m4, autoconf, automake, libtool, gettext, flex, bison, libiconv, make)
# * CMake >= 3.14.0 (Maybe Not Necessary)
# * Python == 3.x.x
# * Meson
# * Ninja
# * FFmpeg == 3.x.x

# ------------------- Dependency -------------------
# Need File: aml-0.3.0.tar.gz
# ----------------- Neat-VNC-0.7.2 -----------------
# Need File: neatvnc-0.7.2.tar.gz

# ##################################################
STORAGE=/home/goufeng

# ############################################ Dependency ############################################

# Function: 构建安装(Build Install) Andri's-Main-Loop-0.3.0
# ##################################################
function Build_Install_Andri_s_Main_Loop_0_3_0() {

    if [[ ! -d "/opt/aml-0.3.0" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( aml-0.3.0 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/aml-0.3.0.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/aml-0.3.0 && meson build/ --prefix=/opt/aml-0.3.0 \
                                              --pkg-config-path=/opt/lib/pkgconfig && \
                                              STEP_BUILDED=1
        
        # ------------------------------------------
        cd $STORAGE/aml-0.3.0 && ninja -C build/ install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # rsync -av /opt/aml-0.3.0/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/aml-0.3.0/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/aml-0.3.0/lib/pkgconfig/aml.pc /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/aml-0.3.0 && return 0
    else
    
        echo "[Caution] Path: ( /opt/aml-0.3.0 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 构建安装(Build Install) Neat-VNC-0.7.2
# ##################################################
function Build_Install_Neat_VNC_0_7_2() {

    # This is a liberally licensed VNC server library that's intended to be fast and neat.
    # ..............................................
    # ### Runtime Dependencies
    #  * aml - https://github.com/any1/aml/
    #  * ffmpeg (optional)
    #  * gbm (optional)
    #  * gnutls (optional)
    #  * libdrm (optional)
    #  * libturbojpeg (optional)
    #  * pixman
    #  * zlib
    # 
    # ### Build Dependencies
    #  * libdrm
    #  * meson
    #  * pkg-config

    if [[ ! -d "/opt/neatvnc-0.7.2" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( neatvnc-0.7.2 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/neatvnc-0.7.2.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # * Problem: ../src/h264-encoder.c:35:10: fatal error: libavutil/hwcontext_drm.h: 没有那个文件或目录
        #             #include <libavutil/hwcontext_drm.h>
        #                      ^~~~~~~~~~~~~~~~~~~~~~~~~~~
        #            compilation terminated.
        #            [25/27] Compiling C object libneatvnc.so.0.0.0.p/src_open-h264.c.o
        #            ninja: build stopped: subcommand failed.
        #   - Solve: 在配置编译 FFmpeg 的时候, 加上 --enable-libdrm 选项。
        cd $STORAGE/neatvnc-0.7.2 && meson build/ --prefix=/opt/neatvnc-0.7.2 \
                                                  --pkg-config-path=/opt/lib/pkgconfig && \
                                                  STEP_BUILDED=1
        
        # ------------------------------------------
        cd $STORAGE/neatvnc-0.7.2 && ninja -C build/ install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # rsync -av /opt/neatvnc-0.7.2/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/neatvnc-0.7.2/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/neatvnc-0.7.2/lib/pkgconfig/neatvnc.pc /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/neatvnc-0.7.2 && return 0
    else
    
        echo "[Caution] Path: ( /opt/neatvnc-0.7.2 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

function main() {

    # ----------------- Dependency -----------------
    Build_Install_Andri_s_Main_Loop_0_3_0
    # ----------------- Neat-VNC-0.7.2 -----------------
    Build_Install_Neat_VNC_0_7_2
}

main
```

## 总结

以上就是关于 Linux运维 Bash脚本 构建安装Neat-VNC-0.7.2 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
