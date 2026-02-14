# 文章_Linux运维_Bash脚本_构建安装GStreamer-1.22.10_GF_2023-03-16

Bash (Bourne Again Shell) 是一个解释器，负责处理 Unix 系统命令行上的命令。它是由 Brian Fox 编写的免费软件，并于 1989 年发布的免费软件，作为 Sh (Bourne Shell) 的替代品。

您可以在 Linux 和 MacOS 机器上使用 Bash，甚至可以通过适用于 Linux 的 Windows 子系统在 Windows 10 机器上使用。

## 使用方法

* 下载源码包:

gstreamer-1.22.10.tar.xz

libdrm-2.4.120.tar.xz

libva-2.19.0.tar.bz2

gst-plugins-base-1.22.10.tar.xz

gst-plugins-good-1.22.10.tar.xz

gst-plugins-bad-1.22.10.tar.xz

gst-plugins-ugly-1.22.10.tar.xz

gst-libav-1.22.10.tar.xz (未测试)

gstreamer-vaapi-1.22.10.tar.xz
  
* 放于指定路径:

这里 Bash Shell 脚本的全局变量 STORAGE 指定的存放源码包的路径 ==/home/goufeng== 可进行修改。
  
* 执行 Bash Shell 脚本:

输入 ==/[路径名]/[脚本名].sh== 即可进行自动编译部署，过程中提示输入 **(y/n)** 输入 **y** 则进行下一步，这样分阶段确认的原因是为了确保能够看到上一个源码编译结果中可能的错误和提示。

## 完整脚本

```shell
#! /bin/bash
# Create By GF 2024-03-16 19:35

# --------------------------------------------------
# Install First: 
# * GNU-Tools (Contains: pkg-config, m4, autoconf, automake, libtool, gettext, flex, bison, libiconv, make)
# * Python == 3.x.x
# * Meson
# * Ninja
# * X11
# * Glib == 2.78.x
# * FFmpeg == 6.x.x (Needed by gst-libav-1.22.10)

# -------------- GStreamer - 1.22.10 ---------------
# Need File: gstreamer-1.22.10.tar.xz
# -------- GStreamer-VAAPI - 1.22.10 - Dep ---------
# Need File: libdrm-2.4.120.tar.xz
# Need File: libva-2.19.0.tar.bz2
# ----------- GStreamer-VAAPI - 1.22.10 ------------
# Need File: gst-plugins-base-1.22.10.tar.xz
# Need File: gst-plugins-good-1.22.10.tar.xz
# Need File: gst-plugins-bad-1.22.10.tar.xz
# Need File: gst-plugins-ugly-1.22.10.tar.xz
# Need File: gst-libav-1.22.10.tar.xz (未测试)
# Need File: gstreamer-vaapi-1.22.10.tar.xz

# ##################################################
# Recommended Optional Installation
# * GTK+-3.24.41 (GTK(GIMP Toolkit) 是一套跨多种平台的图形工具包, 按 LGPL 许可协议发布的。虽然最初是为 GIMP 写的, 但目前已发展为一个功能强大, 设计灵活的一个通用图形库。特别是被 GNOME 选中使得 GTK + 广为流传, 成为 Linux 下开发图形界面的应用程序的主流开发工具之一。目前 GTK + 已经有了成功的 windows 版本。)

# ##################################################
STORAGE=/home/goufeng

# ####################################### GStreamer - 1.22.10 ########################################

# Function: 构建安装(Build Install) GStreamer-1.22.10
# ##################################################
function Build_Install_GStreamer_1_22_10() {

    # GStreamer is an open-source multimedia framework used to build streaming applications, with the goal of simplifying the development of audio/video applications.
    # It has been used to process multimedia data in various formats such as MP3, Ogg, MPEG1, MPEG2, AVI, Quicktime, and more.
    # GStreamer 是用来构建流媒体应用的开源多媒体框架 (Framework), 其目标是要简化 音/视频 应用程序的开发。
    # 已经能够被用来处理像 MP3, Ogg, MPEG1, MPEG2, AVI, Quicktime 等多种格式的多媒体数据。

    if [[ ! -d "/opt/gstreamer-1.22.10" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_NINJA=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( gstreamer-1.22.10 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -Jxvf $STORAGE/gstreamer-1.22.10.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # If you are reinstalling gstreamer from a previous version, it is best if you remove the prior version, including plugins, before installing the new version.
        # If there is a mixture of versions installed, using processes may hang or not work properly. As the root user:
        # 如果要从以前的版本重新安装 gstreamer, 最好在安装新版本之前删除以前的版本, 包括插件。
        # 如果安装了混合版本, 则使用过程可能会挂起或无法正常工作。作为 root 用户:
        # 
        #     rm -rf /usr/bin/gst-* /usr/{lib,libexec}/gstreamer-1.0
        
        # ------------------------------------------
        # Default Build Options:
        # meson  setup ..            \
        #        --prefix=/usr       \
        #        --buildtype=release \
        #        -Dgst_debug=false   \
        #        -Dpackage-origin=https://www.linuxfromscratch.org/blfs/view/svn/ \
        #        -Dpackage-name="GStreamer 1.22.10 BLFS"
        # ..........................................
        cd $STORAGE/gstreamer-1.22.10 && meson build/ --prefix=/opt/gstreamer-1.22.10 \
                                                      --buildtype=release \
                                                      --pkg-config-path=/opt/lib/pkgconfig && \
                                                      STEP_BUILDED=1
                                                
        # ------------------------------------------
        # To test the results, issue: ninja test.
        cd $STORAGE/gstreamer-1.22.10 && ninja && STEP_NINJA=1
        
        # ------------------------------------------
        cd $STORAGE/gstreamer-1.22.10 && ninja -C build/ install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            # Skip # if [[ ! -d "/usr/local/libexec" ]]; then mkdir /usr/local/libexec; fi
            # ......................................
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # ln -sf /opt/gstreamer-1.22.10/bin/* /usr/local/bin/
            # ......................................
            # Skip # rsync -av /opt/gstreamer-1.22.10/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/gstreamer-1.22.10/lib/ /usr/local/lib/
            # ......................................
            # Skip # rsync -av /opt/gstreamer-1.22.10/libexec/ /usr/local/libexec/
            # ......................................
            cp -f /opt/gstreamer-1.22.10/lib/pkgconfig/*.pc /opt/lib/pkgconfig/
            # ......................................
            # Synchronize to sandbox.
            rsync -av /opt/gstreamer-1.22.10/ /opt/sandbox-gstreamer/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/gstreamer-1.22.10 && return 0
    else
    
        echo "[Caution] Path: ( /opt/gstreamer-1.22.10 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ################################# GStreamer-VAAPI - 1.22.10 - Dep ##################################

# Function: 构建安装(Build Install) libdrm-2.4.120
# ##################################################
function Build_Install_libdrm_2_4_120() {

    # Attention: may conflict with the original "drm" in the system.
    # 注意: 可能与系统原有的 "drm" 冲突。

    if [[ ! -d "/opt/libdrm-2.4.120" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( libdrm-2.4.120 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -xvJf $STORAGE/libdrm-2.4.120.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/libdrm-2.4.120 && meson build --prefix=/opt/libdrm-2.4.120 && STEP_BUILDED=1
        
        # ------------------------------------------
        cd $STORAGE/libdrm-2.4.120 && ninja -C build install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # rsync -av /opt/libdrm-2.4.120/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/libdrm-2.4.120/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/libdrm-2.4.120/lib/pkgconfig/*.pc /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/libdrm-2.4.120 && return 0
    else
    
        echo "[Caution] Path: ( /opt/libdrm-2.4.120 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 构建安装(Build Install) libva-2.19.0
# ##################################################
function Build_Install_libva_2_19_0() {

    if [[ ! -d "/opt/libva-2.19.0" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( libva-2.19.0 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -jxvf $STORAGE/libva-2.19.0.tar.bz2 && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/libva-2.19.0 && meson build/ --prefix=/opt/libva-2.19.0 \
                                                 --pkg-config-path=/opt/lib/pkgconfig && \
                                                 STEP_BUILDED=1
        
        # ------------------------------------------
        cd $STORAGE/libva-2.19.0 && ninja -C build/ install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # rsync -av /opt/libva-2.19.0/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/libva-2.19.0/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/libva-2.19.0/lib/pkgconfig/*.pc /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/libva-2.19.0 && return 0
    else
    
        echo "[Caution] Path: ( /opt/libva-2.19.0 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# #################################### GStreamer-VAAPI - 1.22.10 #####################################

# Function: 构建安装(Build Install) gst-plugins-base-1.22.10
# ##################################################
function Build_Install_gst_plugins_base_1_22_10() {

    if [[ ! -d "/opt/gst-plugins-base-1.22.10" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( gst-plugins-base-1.22.10 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -Jxvf $STORAGE/gst-plugins-base-1.22.10.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # Default Build Options:
        # meson  setup ..               \
        #        --prefix=/usr          \
        #        --buildtype=release    \
        #        --wrap-mode=nodownload \
        #        -Dpackage-origin=https://www.linuxfromscratch.org/blfs/view/svn/ \
        #        -Dpackage-name="GStreamer 1.22.10 BLFS"
        # ..........................................
        cd $STORAGE/gst-plugins-base-1.22.10 && meson build/ --prefix=/opt/gst-plugins-base-1.22.10 \
                                                             --buildtype=release \
                                                             --pkg-config-path=/opt/lib/pkgconfig && \
                                                             STEP_BUILDED=1
        
        # ------------------------------------------
        cd $STORAGE/gst-plugins-base-1.22.10 && ninja -C build/ install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # ln -sf /opt/gst-plugins-base-1.22.10/bin/* /usr/local/bin/
            # ......................................
            # Skip # rsync -av /opt/gst-plugins-base-1.22.10/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/gst-plugins-base-1.22.10/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/gst-plugins-base-1.22.10/lib/pkgconfig/*.pc /opt/lib/pkgconfig/
            # ......................................
            # Synchronize to sandbox.
            rsync -av /opt/gst-plugins-base-1.22.10/ /opt/sandbox-gstreamer/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/gst-plugins-base-1.22.10 && return 0
    else
    
        echo "[Caution] Path: ( /opt/gst-plugins-base-1.22.10 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 构建安装(Build Install) gst-plugins-good-1.22.10
# ##################################################
function Build_Install_gst_plugins_good_1_22_10() {

    if [[ ! -d "/opt/gst-plugins-good-1.22.10" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( gst-plugins-good-1.22.10 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -Jxvf $STORAGE/gst-plugins-good-1.22.10.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # Default Build Options:
        # meson setup ..            \
        #       --prefix=/usr       \
        #       --buildtype=release \
        #       -Dpackage-origin=https://www.linuxfromscratch.org/blfs/view/svn/ \
        #       -Dpackage-name="GStreamer 1.22.10 BLFS"
        # ..........................................
        cd $STORAGE/gst-plugins-good-1.22.10 && meson build/ --prefix=/opt/gst-plugins-good-1.22.10 \
                                                             --buildtype=release \
                                                             --pkg-config-path=/opt/lib/pkgconfig && \
                                                             STEP_BUILDED=1
        
        # ------------------------------------------
        cd $STORAGE/gst-plugins-good-1.22.10 && ninja -C build/ install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            # Default None .pc (Pkg-Config) File.
            # ......................................
            # Skip # rsync -av /opt/gst-plugins-good-1.22.10/lib/ /usr/local/lib/
            # ......................................
            # Synchronize to sandbox.
            rsync -av /opt/gst-plugins-good-1.22.10/ /opt/sandbox-gstreamer/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/gst-plugins-good-1.22.10 && return 0
    else
    
        echo "[Caution] Path: ( /opt/gst-plugins-good-1.22.10 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 构建安装(Build Install) gst-plugins-bad-1.22.10
# ##################################################
function Build_Install_gst_plugins_bad_1_22_10() {

    if [[ ! -d "/opt/gst-plugins-bad-1.22.10" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( gst-plugins-bad-1.22.10 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -Jxvf $STORAGE/gst-plugins-bad-1.22.10.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # Default Build Options:
        # meson setup ..            \
        #       --prefix=/usr       \
        #       --buildtype=release \
        #       -Dpackage-origin=https://www.linuxfromscratch.org/blfs/view/svn/ \
        #       -Dpackage-name="GStreamer 1.22.10 BLFS"
        # ..........................................
        cd $STORAGE/gst-plugins-bad-1.22.10 && meson build/ --prefix=/opt/gst-plugins-bad-1.22.10 \
                                                            --buildtype=release \
                                                            --pkg-config-path=/opt/lib/pkgconfig && \
                                                            STEP_BUILDED=1
        
        # ------------------------------------------
        cd $STORAGE/gst-plugins-bad-1.22.10 && ninja -C build/ install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # ln -sf /opt/gst-plugins-bad-1.22.10/bin/* /usr/local/bin/
            # ......................................
            # Skip # rsync -av /opt/gst-plugins-bad-1.22.10/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/gst-plugins-bad-1.22.10/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/gst-plugins-bad-1.22.10/lib/pkgconfig/*.pc /opt/lib/pkgconfig/
            # ......................................
            # Synchronize to sandbox.
            rsync -av /opt/gst-plugins-bad-1.22.10/ /opt/sandbox-gstreamer/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/gst-plugins-bad-1.22.10 && return 0
    else
    
        echo "[Caution] Path: ( /opt/gst-plugins-bad-1.22.10 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 构建安装(Build Install) gst-plugins-ugly-1.22.10
# ##################################################
function Build_Install_gst_plugins_ugly_1_22_10() {

    if [[ ! -d "/opt/gst-plugins-ugly-1.22.10" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( gst-plugins-ugly-1.22.10 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -Jxvf $STORAGE/gst-plugins-ugly-1.22.10.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # Default Build Options:
        # meson  setup ..            \
        #        --prefix=/usr       \
        #        --buildtype=release \
        #        -Dgpl=enabled       \
        #        -Dpackage-origin=https://www.linuxfromscratch.org/blfs/view/svn/ \
        #        -Dpackage-name="GStreamer 1.22.10 BLFS"
        # ..........................................
        cd $STORAGE/gst-plugins-ugly-1.22.10 && meson build/ --prefix=/opt/gst-plugins-ugly-1.22.10 \
                                                             --buildtype=release \
                                                             --pkg-config-path=/opt/lib/pkgconfig && \
                                                             STEP_BUILDED=1
        
        # ------------------------------------------
        cd $STORAGE/gst-plugins-ugly-1.22.10 && ninja -C build/ install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            # Default None .pc (Pkg-Config) File.
            # ......................................
            # Skip # rsync -av /opt/gst-plugins-ugly-1.22.10/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/gst-plugins-ugly-1.22.10/lib/pkgconfig/*.pc /opt/lib/pkgconfig/
            # ......................................
            # Synchronize to sandbox.
            rsync -av /opt/gst-plugins-ugly-1.22.10/ /opt/sandbox-gstreamer/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/gst-plugins-ugly-1.22.10 && return 0
    else
    
        echo "[Caution] Path: ( /opt/gst-plugins-ugly-1.22.10 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 构建安装(Build Install) gst-libav-1.22.10
# ##################################################
function Build_Install_gst_libav_1_22_10() {

    if [[ ! -d "/opt/gst-libav-1.22.10" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( gst-libav-1.22.10 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -Jxvf $STORAGE/gst-libav-1.22.10.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # Default Build Options:
        # meson  setup ..            \
        #        --prefix=/usr       \
        #        --buildtype=release \
        #        -Dpackage-origin=https://www.linuxfromscratch.org/blfs/view/svn/ \
        #        -Dpackage-name="GStreamer 1.22.10 BLFS"
        # ..........................................
        cd $STORAGE/gst-libav-1.22.10 && meson build/ --prefix=/opt/gst-libav-1.22.10 \
                                                      --buildtype=release \
                                                      --pkg-config-path=/opt/lib/pkgconfig && \
                                                      STEP_BUILDED=1
        
        # ------------------------------------------
        cd $STORAGE/gst-libav-1.22.10 && ninja -C build/ install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            # Default None .pc (Pkg-Config) File. (未测试)
            # ......................................
            # Skip # rsync -av /opt/gst-libav-1.22.10/lib/ /usr/local/lib/
            # ......................................
            # Synchronize to sandbox.
            rsync -av /opt/gst-libav-1.22.10/ /opt/sandbox-gstreamer/
            
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/gst-libav-1.22.10 && return 0
    else
    
        echo "[Caution] Path: ( /opt/gst-libav-1.22.10 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 构建安装(Build Install) GStreamer-VAAPI-1.22.10
# ##################################################
function Build_Install_GStreamer_VAAPI_1_22_10() {

    # Gstreamer-vaapi is a collection of GStreamer plugins and helper libraries that allow hardware accelerated video decoding, encoding and processing through VA-API.
    # This package contains GStreamer plugins for VA-API support:
    # Gstreamer-vaapi 是 Gstreamer 插件和帮助程序库的集合, 允许通过 VA-API 进行硬件加速视频解码, 编码和处理。
    # 此包包含用于 VA-API 支持的 GStreamer 插件:
    # ..............................................
    # vaapi<CODEC>dec: 取决于 "CODEC" 的实际值和底层硬件能力, 该插件用于解码 JPEG, MPEG-2, MPEG-4:2, H.264 AVC, H.264 MVC, VP8, VP9, VC-1, WMV3, HEVC 视频到 VA 表面。
    #                  这个插件也可以隐式下载解码表面到原始 YUV 缓冲区。
    # ..............................................
    # vaapi<CODEC>enc: 取决于 "CODEC" 的实际值(mpeg2, h264等)以及硬件能力, 该插件用于编码成 MPEG-2, H.264 AVC, H.264 MVC, JPEG, VP8, VP9, HEVC 视频。
    #                  默认情况下, 生成的是原始格式的比特流, 因此结果可以通过管道传输到 muxer, 例如用于 MP4 容器的 qtmux。
    # ..............................................
    # vaapipostproc: 用于过滤 VA 表面, 例如缩放, deinterlacing (bob, 运动自适应, 运动补偿), 降噪或锐化。
    #                这个插件也用于上传原始YUV像素到VA表面。
    # ..............................................
    # vaapisink: 用于将VA表面渲染到 X11 或 Wayland 显示器。
    #            这个插件还具有一个 "无头" 模式(DRM), 更适合远程转码场景, 具有更快的吞吐量。
    # ..............................................
    # vaapioverlay: 是一种加速合成器, 可以混合或合成不同的视频流。

    if [[ ! -d "/opt/gstreamer-vaapi-1.22.10" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( gstreamer-vaapi-1.22.10 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -Jxvf $STORAGE/gstreamer-vaapi-1.22.10.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # Default Build Options:
        # meson setup ..            \
        #       --prefix=/usr       \
        #       --buildtype=release \
        #       -Dpackage-origin=https://www.linuxfromscratch.org/blfs/view/svn/
        # ..........................................
        cd $STORAGE/gstreamer-vaapi-1.22.10 && meson build/ --prefix=/opt/gstreamer-vaapi-1.22.10 \
                                                            --buildtype=release \
                                                            --pkg-config-path=/opt/lib/pkgconfig && \
                                                            STEP_BUILDED=1
        
        # ------------------------------------------
        cd $STORAGE/gstreamer-vaapi-1.22.10 && ninja -C build/ install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            # Default None .pc (Pkg-Config) File.
            # ......................................
            # Skip # rsync -av /opt/gstreamer-vaapi-1.22.10/lib/ /usr/local/lib/
            # ......................................
            # Synchronize to sandbox.
            rsync -av /opt/gstreamer-vaapi-1.22.10/ /opt/sandbox-gstreamer/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/gstreamer-vaapi-1.22.10 && return 0
    else
    
        echo "[Caution] Path: ( /opt/gstreamer-vaapi-1.22.10 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

function main() {

    # ----------- Compilation Environment ----------
    # 编译 GStreamer 时需要引入 Glib 开发套件的 lib 库文件。
    # >>>>>>>>>>>>>>>>>>>>>>>>> libjpeg-turbo 的 lib 库文件。
    # >>>>>>>>>>>>>>>>>>>>>>>>> Fribidi 的 lib 库文件。
    # 编译 gst-plugins-base 时需要引入 udev 的 lib 库文件。
    # 编译 gst-plugins-good 时需要引入 libdrm 的 lib 库文件。
    export LIBRARY_PATH=/opt/sandbox-glib/lib:/opt/libjpeg-turbo-3.0.0/lib:/opt/fribidi-1.0.13/lib:/opt/eudev-3.2.14/lib:/opt/libdrm-2.4.120/lib
    export LD_LIBRARY_PATH=/opt/sandbox-glib/lib:/opt/libjpeg-turbo-3.0.0/lib:/opt/fribidi-1.0.13/lib:/opt/eudev-3.2.14/lib:/opt/libdrm-2.4.120/lib
    # ..............................................
    # 编译 GStreamer 时需要引入 Glib 开发套件的 bin 二进制文件。
    export PATH=$PATH:/opt/sandbox-glib/bin

    # ------------ GStreamer - 1.22.10 -------------
    Build_Install_GStreamer_1_22_10
    # ------ GStreamer-VAAPI - 1.22.10 - Dep -------
    Build_Install_libdrm_2_4_120
    Build_Install_libva_2_19_0
    # --------- GStreamer-VAAPI - 1.22.10 ----------
    Build_Install_gst_plugins_base_1_22_10
    Build_Install_gst_plugins_good_1_22_10
    Build_Install_gst_plugins_bad_1_22_10
    Build_Install_gst_plugins_ugly_1_22_10
    # Skip # Build_Install_gst_libav_1_22_10 #(未测试)
    Build_Install_GStreamer_VAAPI_1_22_10
}

main
```

## 总结

以上就是关于 Linux运维 Bash脚本 构建安装GStreamer-1.22.10 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
