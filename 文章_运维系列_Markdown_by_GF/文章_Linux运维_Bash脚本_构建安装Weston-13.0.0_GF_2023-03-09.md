# 文章_Linux运维_Bash脚本_构建安装Weston-13.0.0_GF_2023-03-09

Bash (Bourne Again Shell) 是一个解释器，负责处理 Unix 系统命令行上的命令。它是由 Brian Fox 编写的免费软件，并于 1989 年发布的免费软件，作为 Sh (Bourne Shell) 的替代品。

您可以在 Linux 和 MacOS 机器上使用 Bash，甚至可以通过适用于 Linux 的 Windows 子系统在 Windows 10 机器上使用。

## 使用方法

* 下载源码包:

xcb-util-0.4.1.tar.xz

xcb-util-image-0.4.1.tar.xz

xcb-util-renderutil-0.3.10.tar.xz

xcb-util-cursor-0.1.4.tar.xz

libXcursor-1.2.0.tar.bz2

eudev-3.2.14.tar.gz (udev-251)

mtdev-1.1.6.tar.gz

libevdev-1.11.0.tar.xz

libgudev-238.tar.xz

pyudev-0.24.1.tar.gz (Python 源码)

libevdev-0.11.tar.gz (Python 源码)

tomli-2.0.1.tar.gz (Python 源码)

iniconfig-2.0.0.tar.gz (Python 源码)

exceptiongroup-1.2.0.tar.gz (Python 源码)

pluggy-1.4.0.tar.gz (Python 源码)

packaging-23.2.tar.gz (Python 源码)

pytest-8.1.0.tar.gz (Python 源码)

libwacom-2.10.0.tar.xz

Linux-PAM-1.5.2.tar.xz

libxkbcommon-1.6.0.tar.xz

check-0.15.2.tar.gz

libinput-1.25.0.tar.gz

libwebp-1.3.1.tar.gz

seatd-0.8.0.tar.gz

lcms2-2.14.tar.gz

libva-2.19.0.tar.bz2

pipewire-0.3.77.tar.gz

weston-13.0.0.tar.xz
  
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
# * CMake >= 3.14.0
# * Python == 3.x.x
# * Meson
# * Ninja
# * X11
# * Glib
# * libGD == 2.3.3 (Compiled by: freetype, libpng, jpeg)
# * Wayland == 1.22.0 (Contains: Wayland-Protocols)
# * Mesa(OpenGL) == 23.3.6 (Needed by GTK+)
# * Pango == 1.51.x (Contains: Fribidi, FreeType, Fontconfig / Needed by libinput)
# * GTK+ == 3.24.41 (Needed by libinput)
# * FFmpeg == 3.x.x (Optional: Needed by FreeRDP2)
# * FreeRDP2 == 2.3.x (Optional)
# * Neat-VNC == 0.7.2 (Optional)
# * Systemd == 250 (Optional)
# * GStreamer1.0 (Optional)

# ---------------- X11 - libXcursor ----------------
# Need File: xcb-util-0.4.1.tar.xz
# Need File: xcb-util-image-0.4.1.tar.xz
# Need File: xcb-util-renderutil-0.3.10.tar.xz
# Need File: xcb-util-cursor-0.1.4.tar.xz
# Need File: libXcursor-1.2.0.tar.bz2
# -------- libinput Dep: libwacom (Optional) -------
# Need File: eudev-3.2.14.tar.gz (udev-251)
# Need File: mtdev-1.1.6.tar.gz
# Need File: libevdev-1.11.0.tar.xz
# Need File: libgudev-238.tar.xz
# Need File: pyudev-0.24.1.tar.gz (Python 源码)
# Need File: libevdev-0.11.tar.gz (Python 源码)
# Need File: tomli-2.0.1.tar.gz (Python 源码)
# Need File: iniconfig-2.0.0.tar.gz (Python 源码)
# Need File: exceptiongroup-1.2.0.tar.gz (Python 源码)
# Need File: pluggy-1.4.0.tar.gz (Python 源码)
# Need File: packaging-23.2.tar.gz (Python 源码)
# Need File: pytest-8.1.0.tar.gz (Python 源码)
# Need File: libwacom-2.10.0.tar.xz
# --- Weston (Base Wayland Proto) Dep: Linux-PAM ---
# Need File: Linux-PAM-1.5.2.tar.xz
# ---- Weston (Base Wayland Protocol) Dependency ---
# Need File: libxkbcommon-1.6.0.tar.xz
# Need File: check-0.15.2.tar.gz
# Need File: libinput-1.25.0.tar.gz
# Need File: libwebp-1.3.1.tar.gz
# Need File: seatd-0.8.0.tar.gz
# Need File: lcms2-2.14.tar.gz
# Need File: libva-2.19.0.tar.bz2
# Need File: pipewire-0.3.77.tar.gz
# --------- Weston (Base Wayland Protocol) ---------
# Need File: weston-13.0.0.tar.xz

# ##################################################
STORAGE=/home/goufeng

# ######################################### X11 - libXcursor #########################################

# Function: 编译安装(Compile Install) xcb-util-0.4.1
# ##################################################
function Compile_Install_xcb_util_0_4_1() {

    if [[ ! -d "/opt/xcb-util-0.4.1" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( xcb-util-0.4.1 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -Jxvf $STORAGE/xcb-util-0.4.1.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/xcb-util-0.4.1 && ./configure --prefix=/opt/xcb-util-0.4.1 \
                                                  PKG_CONFIG_PATH="/opt/lib/pkgconfig" && \
                                                  STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # rsync -av /opt/xcb-util-0.4.1/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/xcb-util-0.4.1/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/xcb-util-0.4.1/lib/pkgconfig/*.pc /opt/lib/pkgconfig/
            # ......................................
            # Synchronize to sandbox.
            rsync -av /opt/xcb-util-0.4.1/ /opt/sandbox-X11/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/xcb-util-0.4.1 && return 0
    else
    
        echo "[Caution] Path: ( /opt/xcb-util-0.4.1 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) xcb-util-image-0.4.1
# ##################################################
function Compile_Install_xcb_util_image_0_4_1() {

    if [[ ! -d "/opt/xcb-util-image-0.4.1" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( xcb-util-image-0.4.1 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -Jxvf $STORAGE/xcb-util-image-0.4.1.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/xcb-util-image-0.4.1 && ./configure --prefix=/opt/xcb-util-image-0.4.1 \
                                                        PKG_CONFIG_PATH="/opt/lib/pkgconfig" && \
                                                        STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # rsync -av /opt/xcb-util-image-0.4.1/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/xcb-util-image-0.4.1/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/xcb-util-image-0.4.1/lib/pkgconfig/xcb-image.pc /opt/lib/pkgconfig/
            # ......................................
            # Synchronize to sandbox.
            rsync -av /opt/xcb-util-image-0.4.1/ /opt/sandbox-X11/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/xcb-util-image-0.4.1 && return 0
    else
    
        echo "[Caution] Path: ( /opt/xcb-util-image-0.4.1 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) xcb-util-renderutil-0.3.10
# ##################################################
function Compile_Install_xcb_util_renderutil_0_3_10() {

    if [[ ! -d "/opt/xcb-util-renderutil-0.3.10" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( xcb-util-renderutil-0.3.10 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -Jxvf $STORAGE/xcb-util-renderutil-0.3.10.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/xcb-util-renderutil-0.3.10 && ./configure --prefix=/opt/xcb-util-renderutil-0.3.10 \
                                                              PKG_CONFIG_PATH="/opt/lib/pkgconfig" && \
                                                              STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # rsync -av /opt/xcb-util-renderutil-0.3.10/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/xcb-util-renderutil-0.3.10/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/xcb-util-renderutil-0.3.10/lib/pkgconfig/xcb-renderutil.pc /opt/lib/pkgconfig/
            # ......................................
            # Synchronize to sandbox.
            rsync -av /opt/xcb-util-renderutil-0.3.10/ /opt/sandbox-X11/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/xcb-util-renderutil-0.3.10 && return 0
    else
    
        echo "[Caution] Path: ( /opt/xcb-util-renderutil-0.3.10 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) xcb-util-cursor-0.1.4
# ##################################################
function Compile_Install_xcb_util_cursor_0_1_4() {

    if [[ ! -d "/opt/xcb-util-cursor-0.1.4" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( xcb-util-cursor-0.1.4 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -Jxvf $STORAGE/xcb-util-cursor-0.1.4.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/xcb-util-cursor-0.1.4 && ./configure --prefix=/opt/xcb-util-cursor-0.1.4 \
                                                         PKG_CONFIG_PATH="/opt/lib/pkgconfig" && \
                                                         STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # rsync -av /opt/xcb-util-cursor-0.1.4/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/xcb-util-cursor-0.1.4/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/xcb-util-cursor-0.1.4/lib/pkgconfig/xcb-cursor.pc /opt/lib/pkgconfig/
            # ......................................
            # Synchronize to sandbox.
            rsync -av /opt/xcb-util-cursor-0.1.4/ /opt/sandbox-X11/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/xcb-util-cursor-0.1.4 && return 0
    else
    
        echo "[Caution] Path: ( /opt/xcb-util-cursor-0.1.4 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) libXcursor-1.2.0
# ##################################################
function Compile_Install_libXcursor_1_2_0() {

    if [[ ! -d "/opt/libXcursor-1.2.0" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( libXcursor-1.2.0 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -jxvf $STORAGE/libXcursor-1.2.0.tar.bz2 && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/libXcursor-1.2.0 && ./configure --prefix=/opt/libXcursor-1.2.0 \
                                                    PKG_CONFIG_PATH="/opt/lib/pkgconfig" && \
                                                    STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # rsync -av /opt/libXcursor-1.2.0/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/libXcursor-1.2.0/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/libXcursor-1.2.0/lib/pkgconfig/xcursor.pc /opt/lib/pkgconfig/
            # ......................................
            # Synchronize to sandbox.
            rsync -av /opt/libXcursor-1.2.0/ /opt/sandbox-X11/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/libXcursor-1.2.0 && return 0
    else
    
        echo "[Caution] Path: ( /opt/libXcursor-1.2.0 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ################################# libinput Dep: libwacom (Optional) ################################

# Function: 编译安装(Compile Install) eudev-3.2.14
# ##################################################
function Compile_Install_eudev_3_2_14() {

    # Attention: may conflict with the original "udev" in the system.
    # 注意: 可能与系统原有的 "udev" 冲突。

    # eudev 提供针对内核提供的 udev 设备管理服务的函数库。
    # udev 是 Linux 2.6 内核的设备管理器。
    # udev 它在 /dev 目录下动态地 创建/移除 设备节点, 用于在系统中传递解决方案的有关设备信息, 以及在出现设备事件 (如删除、插入设备) 时触发相应的操作。

    if [[ ! -d "/opt/eudev-3.2.14" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( eudev-3.2.14 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/eudev-3.2.14.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/eudev-3.2.14 && ./configure --prefix=/opt/eudev-3.2.14 && STEP_BUILDED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # Skip # if [[ ! -d "/usr/local/sbin" ]]; then mkdir /usr/local/sbin; fi
            # ......................................
            # Skip # ln -sf /opt/eudev-3.2.14/bin/udevadm /usr/local/bin/
            # Skip # ln -sf /opt/eudev-3.2.14/bin/udevadm /usr/local/sbin/udevadm
            # ......................................
            # Skip # ln -sf /opt/eudev-3.2.14/sbin/udevd /usr/local/sbin/
            # ......................................
            # Skip # rsync -av /opt/eudev-3.2.14/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/eudev-3.2.14/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/eudev-3.2.14/lib/pkgconfig/libudev.pc /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/eudev-3.2.14 && return 0
    else
    
        echo "[Caution] Path: ( /opt/eudev-3.2.14 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) mtdev-1.1.6
# ##################################################
function Compile_Install_mtdev_1_1_6() {

    # Attention: may conflict with the original "mtdev" in the system.
    # 注意: 可能与系统原有的 "mtdev" 冲突。

    # mtdev 是一个用于处理多点触摸设备输入的库。
    # mtdev 可以解析多点触摸设备的输入数据, 并将其转换为适合应用程序处理的格式。

    if [[ ! -d "/opt/mtdev-1.1.6" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( mtdev-1.1.6 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/mtdev-1.1.6.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/mtdev-1.1.6 && ./configure --prefix=/opt/mtdev-1.1.6 && STEP_BUILDED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # ln -sf /opt/mtdev-1.1.6/bin/* /usr/local/bin/
            # ......................................
            # Skip # rsync -av /opt/mtdev-1.1.6/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/mtdev-1.1.6/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/mtdev-1.1.6/lib/pkgconfig/mtdev.pc /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/mtdev-1.1.6 && return 0
    else
    
        echo "[Caution] Path: ( /opt/mtdev-1.1.6 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) libevdev-1.11.0
# ##################################################
function Compile_Install_libevdev_1_11_0() {

    # Attention: may conflict with the original "evdev" in the system.
    # 注意: 可能与系统原有的 "evdev" 冲突。
    # ..............................................
    # evdev 是一种仅限 Linux 的通用协议, 内核使用该协议将有关输入设备的信息和事件转发给用户空间。
    # 这不只是对鼠标和键盘, 而是任何形式的轴, 键或按钮, 包括像摄像头和遥控装置。每个设备都以 /dev/input/event0 的形式表示为设备节点, 随着您添加更多设备, 尾随数字会增加。
    # 考虑一种场景, 针对触摸屏, 需要在后台模拟用户的点击操作:
    # * Kernel 提供一种机制, 可以在 userspace 模拟 input devices, 称之为 uinput。
    # * uinput 即用户在用户空间模拟输入设备, 比如模拟触摸屏的点击操作。
    # * 则可以基于 libevdev 函数库, 通过 Kernel 下的 uinput 机制, 生成虚假的 /dev/input/eventX 设备, 然后发送触摸屏的坐标以及点击事件, 模拟用户的点击滑动等操作。

    if [[ ! -d "/opt/libevdev-1.11.0" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( libevdev-1.11.0 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -xvJf $STORAGE/libevdev-1.11.0.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/libevdev-1.11.0 && ./configure --prefix=/opt/libevdev-1.11.0 && STEP_BUILDED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # ln -sf /opt/libevdev-1.11.0/bin/* /usr/local/bin/
            # ......................................
            # Skip # rsync -av /opt/libevdev-1.11.0/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/libevdev-1.11.0/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/libevdev-1.11.0/lib/pkgconfig/libevdev.pc /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/libevdev-1.11.0 && return 0
    else
    
        echo "[Caution] Path: ( /opt/libevdev-1.11.0 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 构建安装(Build Install) libgudev-238
# ##################################################
function Build_Install_libgudev_238() {

    # Attention: may conflict with the original "gudev" in the system.
    # 注意: 可能与系统原有的 "gudev" 冲突。

    if [[ ! -d "/opt/libgudev-238" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( libgudev-238 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -xvJf $STORAGE/libgudev-238.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/libgudev-238 && meson build/ --prefix=/opt/libgudev-238 \
                                                 --pkg-config-path=/opt/lib/pkgconfig && \
                                                 STEP_BUILDED=1
        
        # ------------------------------------------
        cd $STORAGE/libgudev-238 && ninja -C build/ install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # rsync -av /opt/libgudev-238/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/libgudev-238/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/libgudev-238/lib/pkgconfig/gudev-1.0.pc /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/libgudev-238 && return 0
    else
    
        echo "[Caution] Path: ( /opt/libgudev-238 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 构建安装(Build Install) pyudev-0.24.1 (by Python3)
# ##################################################
function Build_Install_pyudev_0_24_1_by_Python3() {

    # 使用 expr index "$string" "$substring" 来判断字符串 $string 中是否包含子字符串 $substring。
    # Use the expr index "$string" and "$substring" to determine whether the string $string contains a substring $substring.
    
    # 如果子字符串存在, 则返回子字符串在原字符串中的位置 (从 1 开始), 否则返回 0。
    # If the substring exists, return the position of the substring in the original string (starting from 1), otherwise return 0.
    
    local EXISTS_LINE=$(pip3 list | grep "pyudev")
    local EXISTS_NAME=$(expr index "$EXISTS_LINE" "pyudev")
    local EXISTS_VERSION=$(expr index "$EXISTS_LINE" "0.24.1")

    if [[ $EXISTS_NAME == 0 && $EXISTS_VERSION == 0 ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( pyudev-0.24.1 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/pyudev-0.24.1.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/pyudev-0.24.1 && python3 setup.py build && STEP_BUILDED=1
        
        # ------------------------------------------
        cd $STORAGE/pyudev-0.24.1 && python3 setup.py install && STEP_INSTALLED=1

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/pyudev-0.24.1 && return 0
    else
    
        echo "[Caution] Python Program: ( pyudev-0.24.1 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 构建安装(Build Install) libevdev-0.11 (by Python3)
# ##################################################
function Build_Install_libevdev_0_11_by_Python3() {

    # 使用 expr index "$string" "$substring" 来判断字符串 $string 中是否包含子字符串 $substring。
    # Use the expr index "$string" and "$substring" to determine whether the string $string contains a substring $substring.
    
    # 如果子字符串存在, 则返回子字符串在原字符串中的位置 (从 1 开始), 否则返回 0。
    # If the substring exists, return the position of the substring in the original string (starting from 1), otherwise return 0.
    
    local EXISTS_LINE=$(pip3 list | grep "libevdev")
    local EXISTS_NAME=$(expr index "$EXISTS_LINE" "libevdev")
    local EXISTS_VERSION=$(expr index "$EXISTS_LINE" "0.11")

    if [[ $EXISTS_NAME == 0 && $EXISTS_VERSION == 0 ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( libevdev-0.11 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/libevdev-0.11.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/libevdev-0.11 && python3 setup.py build && STEP_BUILDED=1
        
        # ------------------------------------------
        cd $STORAGE/libevdev-0.11 && python3 setup.py install && STEP_INSTALLED=1

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/libevdev-0.11 && return 0
    else
    
        echo "[Caution] Python Program: ( libevdev-0.11 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: Pip安装(Pip Install) tomli-2.0.1 (by Python3)
# ##################################################
function Pip_Install_tomli_2_0_1_by_Python3() {

    # 使用 expr index "$string" "$substring" 来判断字符串 $string 中是否包含子字符串 $substring。
    # Use the expr index "$string" and "$substring" to determine whether the string $string contains a substring $substring.
    
    # 如果子字符串存在, 则返回子字符串在原字符串中的位置 (从 1 开始), 否则返回 0。
    # If the substring exists, return the position of the substring in the original string (starting from 1), otherwise return 0.
    
    local EXISTS_LINE=$(pip3 list | grep "tomli")
    local EXISTS_NAME=$(expr index "$EXISTS_LINE" "tomli")
    local EXISTS_VERSION=$(expr index "$EXISTS_LINE" "2.0.1")

    if [[ $EXISTS_NAME == 0 && $EXISTS_VERSION == 0 ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Pip Install ( tomli-2.0.1 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/tomli-2.0.1.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # 如果项目位于其他目录, 则需要将其路径 "." 替换。
        # pip 工具会根据项目中的 pyproject.toml 文件自动安装相应的依赖项。
        cd $STORAGE/tomli-2.0.1 && pip3 install . && STEP_INSTALLED=1

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/tomli-2.0.1 && return 0
    else
    
        echo "[Caution] Python Program: ( tomli-2.0.1 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: Pip安装(Pip Install) iniconfig-2.0.0 (by Python3)
# ##################################################
function Pip_Install_iniconfig_2_0_0_by_Python3() {

    # 使用 expr index "$string" "$substring" 来判断字符串 $string 中是否包含子字符串 $substring。
    # Use the expr index "$string" and "$substring" to determine whether the string $string contains a substring $substring.
    
    # 如果子字符串存在, 则返回子字符串在原字符串中的位置 (从 1 开始), 否则返回 0。
    # If the substring exists, return the position of the substring in the original string (starting from 1), otherwise return 0.
    
    local EXISTS_LINE=$(pip3 list | grep "iniconfig")
    local EXISTS_NAME=$(expr index "$EXISTS_LINE" "iniconfig")
    local EXISTS_VERSION=$(expr index "$EXISTS_LINE" "2.0.0")

    if [[ $EXISTS_NAME == 0 && $EXISTS_VERSION == 0 ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Pip Install ( iniconfig-2.0.0 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/iniconfig-2.0.0.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # 如果项目位于其他目录, 则需要将其路径 "." 替换。
        # pip 工具会根据项目中的 pyproject.toml 文件自动安装相应的依赖项。
        cd $STORAGE/iniconfig-2.0.0 && pip3 install . && STEP_INSTALLED=1

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/iniconfig-2.0.0 && return 0
    else
    
        echo "[Caution] Python Program: ( iniconfig-2.0.0 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: Pip安装(Pip Install) exceptiongroup-1.2.0 (by Python3)
# ##################################################
function Pip_Install_exceptiongroup_1_2_0_by_Python3() {

    # 使用 expr index "$string" "$substring" 来判断字符串 $string 中是否包含子字符串 $substring。
    # Use the expr index "$string" and "$substring" to determine whether the string $string contains a substring $substring.
    
    # 如果子字符串存在, 则返回子字符串在原字符串中的位置 (从 1 开始), 否则返回 0。
    # If the substring exists, return the position of the substring in the original string (starting from 1), otherwise return 0.
    
    local EXISTS_LINE=$(pip3 list | grep "exceptiongroup")
    local EXISTS_NAME=$(expr index "$EXISTS_LINE" "exceptiongroup")
    local EXISTS_VERSION=$(expr index "$EXISTS_LINE" "1.2.0")

    if [[ $EXISTS_NAME == 0 && $EXISTS_VERSION == 0 ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Pip Install ( exceptiongroup-1.2.0 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/exceptiongroup-1.2.0.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # 如果项目位于其他目录, 则需要将其路径 "." 替换。
        # pip 工具会根据项目中的 pyproject.toml 文件自动安装相应的依赖项。
        cd $STORAGE/exceptiongroup-1.2.0 && pip3 install . && STEP_INSTALLED=1

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/exceptiongroup-1.2.0 && return 0
    else
    
        echo "[Caution] Python Program: ( exceptiongroup-1.2.0 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 构建安装(Build Install) pluggy-1.4.0 (by Python3)
# ##################################################
function Build_Install_pluggy_1_4_0_by_Python3() {

    # 使用 expr index "$string" "$substring" 来判断字符串 $string 中是否包含子字符串 $substring。
    # Use the expr index "$string" and "$substring" to determine whether the string $string contains a substring $substring.
    
    # 如果子字符串存在, 则返回子字符串在原字符串中的位置 (从 1 开始), 否则返回 0。
    # If the substring exists, return the position of the substring in the original string (starting from 1), otherwise return 0.
    
    local EXISTS_LINE=$(pip3 list | grep "pluggy")
    local EXISTS_NAME=$(expr index "$EXISTS_LINE" "pluggy")
    local EXISTS_VERSION=$(expr index "$EXISTS_LINE" "1.4.0")

    if [[ $EXISTS_NAME == 0 && $EXISTS_VERSION == 0 ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( pluggy-1.4.0 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/pluggy-1.4.0.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/pluggy-1.4.0 && python3 setup.py build && STEP_BUILDED=1
        
        # ------------------------------------------
        cd $STORAGE/pluggy-1.4.0 && python3 setup.py install && STEP_INSTALLED=1

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/pluggy-1.4.0 && return 0
    else
    
        echo "[Caution] Python Program: ( pluggy-1.4.0 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: Pip安装(Pip Install) Packaging-23.2 (by Python3)
# ##################################################
function Pip_Install_Packaging_23_2_by_Python3() {

    # 使用 expr index "$string" "$substring" 来判断字符串 $string 中是否包含子字符串 $substring。
    # Use the expr index "$string" and "$substring" to determine whether the string $string contains a substring $substring.
    
    # 如果子字符串存在, 则返回子字符串在原字符串中的位置 (从 1 开始), 否则返回 0。
    # If the substring exists, return the position of the substring in the original string (starting from 1), otherwise return 0.
    
    local EXISTS_LINE=$(pip3 list | grep "packaging")
    local EXISTS_NAME=$(expr index "$EXISTS_LINE" "packaging")
    local EXISTS_VERSION=$(expr index "$EXISTS_LINE" "23.2")

    if [[ $EXISTS_NAME == 0 && $EXISTS_VERSION == 0 ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Pip Install ( packaging-23.2 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/packaging-23.2.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # 如果项目位于其他目录, 则需要将其路径 "." 替换。
        # pip 工具会根据项目中的 pyproject.toml 文件自动安装相应的依赖项。
        cd $STORAGE/packaging-23.2 && pip3 install . && STEP_INSTALLED=1

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/packaging-23.2 && return 0
    else
    
        echo "[Caution] Python Program: ( packaging-23.2 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: Pip安装(Pip Install) pytest-8.1.0 (by Python3)
# ##################################################
function Pip_Install_pytest_8_1_0_by_Python3() {

    # 使用 expr index "$string" "$substring" 来判断字符串 $string 中是否包含子字符串 $substring。
    # Use the expr index "$string" and "$substring" to determine whether the string $string contains a substring $substring.
    
    # 如果子字符串存在, 则返回子字符串在原字符串中的位置 (从 1 开始), 否则返回 0。
    # If the substring exists, return the position of the substring in the original string (starting from 1), otherwise return 0.
    
    local EXISTS_LINE=$(pip3 list | grep "pytest")
    local EXISTS_NAME=$(expr index "$EXISTS_LINE" "pytest")
    local EXISTS_VERSION=$(expr index "$EXISTS_LINE" "8.1.0")

    if [[ $EXISTS_NAME == 0 && $EXISTS_VERSION == 0 ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Pip Install ( pytest-8.1.0 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/pytest-8.1.0.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # 如果项目位于其他目录, 则需要将其路径 "." 替换。
        # pip 工具会根据项目中的 pyproject.toml 文件自动安装相应的依赖项。
        cd $STORAGE/pytest-8.1.0 && pip3 install . && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            ln -sf /opt/Python-3.8.0/bin/pytest /usr/local/bin/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/pytest-8.1.0 && return 0
    else
    
        echo "[Caution] Python Program: ( pytest-8.1.0 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 构建安装(Build Install) libwacom-2.10.0
# ##################################################
function Build_Install_libwacom_2_10_0() {

    # libwacom 用于识别 Wacom 数位板及其特定于模型的功能。通过它可以轻松访问诸如 "这是内置屏幕平板电脑", "此型号的尺寸是多少" 之类的信息。
    # 例如, GNOME 当前使用此功能将内置平板电脑映射到正确的屏幕。
    # GNOME 环境中的 Wacom Tablet 设置面板中的工具以及 libinput 堆栈都使用 libwacom 平板电脑客户端库, 它存储了有关 Wacom 平板电脑的数据。
    # 如果要在 libwacom 库中添加对新平板电脑的支持，您必须确保此新平板电脑的定义文件存在。

    if [[ ! -d "/opt/libwacom-2.10.0" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( libwacom-2.10.0 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -xvJf $STORAGE/libwacom-2.10.0.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # * Problem: >>> import libevdev
        #            Traceback (most recent call last):
        #              File "<stdin>", line 1, in <module>
        #              File "<frozen importlib._bootstrap>", line 991, in _find_and_load
        #              File "<frozen importlib._bootstrap>", line 975, in _find_and_load_unlocked
        #              File "<frozen importlib._bootstrap>", line 655, in _load_unlocked
        #              File "<frozen importlib._bootstrap>", line 618, in _load_backward_compatible
        #              File "<frozen zipimport>", line 259, in load_module
        #              File "/opt/Python-3.8.0/lib/python3.8/site-packages/libevdev-0.11-py3.8.egg/libevdev/__init__.py", line 23, in <module>
        #            ......
        #                func = self.__getitem__(name)
        #              File "/opt/Python-3.8.0/lib/python3.8/ctypes/__init__.py", line 387, in __getitem__
        #                func = self._FuncPtr((name_or_ordinal, self))
        #            AttributeError: /usr/lib/x86_64-linux-gnu/libevdev.so.2: undefined symbol: libevdev_event_value_get_name
        #   - Solve: Python3 在 import libevdev 的时候, 由于没有将 Linux 安装的目标 libevdev 的 libevdev.so.x 加入动态库可查找路径, 因此只找到系统原有的 libevdev。
        #            执行命令: export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/libevdev-1.11.0/lib
        export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/libevdev-1.11.0/lib
        # ..........................................
        # * Problem: /opt/libgudev-238/lib/libgudev-1.0.so: 对 'udev_device_get_current_tags_list_entry@LIBUDEV_247' 未定义的引用。
        #   - Solve: 编译过程在调用 udev 的时候, 由于没有将 Linux 安装的目标 eudev 中的动态库加入可查找路径, 没有调用到 udev-251 因此只找到系统原有的 udev。
        #            执行命令: export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/eudev-3.2.14/lib
        export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/eudev-3.2.14/lib
        
        # ------------------------------------------
        cd $STORAGE/libwacom-2.10.0 && meson build/ --prefix=/opt/libwacom-2.10.0 \
                                                    --pkg-config-path=/opt/lib/pkgconfig && \
                                                    STEP_BUILDED=1
        
        # ------------------------------------------
        cd $STORAGE/libwacom-2.10.0 && ninja -C build/ install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # ln -sf /opt/libwacom-2.10.0/bin/* /usr/local/bin/
            # ......................................
            # Skip # rsync -av /opt/libwacom-2.10.0/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/libwacom-2.10.0/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/libwacom-2.10.0/lib/pkgconfig/libwacom.pc /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/libwacom-2.10.0 && return 0
    else
    
        echo "[Caution] Path: ( /opt/libwacom-2.10.0 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ############################ Weston (Base Wayland Proto) Dep: Linux-PAM ############################

# Function: 编译安装(Compile Install) Linux-PAM-1.5.2
# ##################################################
function Compile_Install_Linxu_PAM_1_5_2() {

    if [[ ! -d "/opt/Linux-PAM-1.5.2" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( Linux-PAM-1.5.2 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -xvJf $STORAGE/Linux-PAM-1.5.2.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # Default Configure Options:
        # ./configure --prefix=/usr \
        #             --sbindir=/usr/sbin \
        #             --sysconfdir=/etc \
        #             --libdir=/usr/lib  \
        #             --enable-securedir=/usr/lib/security \
        #             --docdir=/usr/share/doc/Linux-PAM-1.5.2
        cd $STORAGE/Linux-PAM-1.5.2 && ./configure --prefix=/opt/Linux-PAM-1.5.2 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            # ......................................
            # Create a subdirectory "security" for Include.
            if [[ ! -d "/opt/Linux-PAM-1.5.2/include/security" ]]; then mkdir /opt/Linux-PAM-1.5.2/include/security; fi
            # ......................................
            cp -f /opt/Linux-PAM-1.5.2/include/*.h /opt/Linux-PAM-1.5.2/include/security/
            # ......................................
            # Regular synchronization file path.
            # Skip # if [[ ! -d "/usr/local/sbin" ]]; then mkdir /usr/local/sbin; fi
            # ......................................
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # ln -sf /opt/Linux-PAM-1.5.2/sbin/* /usr/local/sbin/
            # ......................................
            # Skip # rsync -av /opt/Linux-PAM-1.5.2/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/Linux-PAM-1.5.2/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/Linux-PAM-1.5.2/lib/pkgconfig/*.pc /opt/lib/pkgconfig/
        fi
        
        # ------------------------------------------
        # 将 PAM 加入系统服务 (for Ubuntu 18.04)。
        # Skip # ln -s /opt/Linux-PAM-1.5.2/lib/systemd/system/pam_namespace.service /lib/systemd/system/pam.service

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/Linux-PAM-1.5.2 && return 0
    else
    
        echo "[Caution] Path: ( /opt/Linux-PAM-1.5.2 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ############################# Weston (Base Wayland Protocol) Dependency ############################

# Function: 构建安装(Build Install) libxkbcommon-1.6.0
# ##################################################
function Build_Install_libxkbcommon_1_6_0() {

    # xkbcommon is a library for handling of keyboard descriptions, including loading them from disk, parsing them and handling their state.
    # xkbcommon 是一个用于处理键盘描述的库, 包括从磁盘加载、解析和处理它们的状态。
    # It's mainly meant for client toolkits, window systems, and other system applications.
    # 它主要用于客户端工具包、窗口系统和其他系统应用程序。

    if [[ ! -d "/opt/libxkbcommon-1.6.0" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( libxkbcommon-1.6.0 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -xvJf $STORAGE/libxkbcommon-1.6.0.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/libxkbcommon-1.6.0 && meson build/ --prefix=/opt/libxkbcommon-1.6.0 \
                                                       --pkg-config-path=/opt/lib/pkgconfig && \
                                                       STEP_BUILDED=1
        
        # ------------------------------------------
        cd $STORAGE/libxkbcommon-1.6.0 && ninja -C build/ install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # Skip # if [[ ! -d "/usr/local/libexec" ]]; then mkdir /usr/local/libexec; fi
            # ......................................
            # Skip # ln -sf /opt/libxkbcommon-1.6.0/bin/* /usr/local/bin/
            # ......................................
            # Skip # rsync -av /opt/libxkbcommon-1.6.0/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/libxkbcommon-1.6.0/lib/ /usr/local/lib/
            # ......................................
            # Skip # rsync -av /opt/libxkbcommon-1.6.0/libexec/ /usr/local/libexec/
            # ......................................
            cp -f /opt/libxkbcommon-1.6.0/lib/pkgconfig/xkbcommon.pc     /opt/lib/pkgconfig/
            cp -f /opt/libxkbcommon-1.6.0/lib/pkgconfig/xkbcommon-x11.pc /opt/lib/pkgconfig/
            cp -f /opt/libxkbcommon-1.6.0/lib/pkgconfig/xkbregistry.pc   /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/libxkbcommon-1.6.0 && return 0
    else
    
        echo "[Caution] Path: ( /opt/libxkbcommon-1.6.0 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) check-0.15.2
# ##################################################
function Compile_Install_check_0_15_2() {

    if [[ ! -d "/opt/check-0.15.2" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( check-0.15.2 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/check-0.15.2.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/check-0.15.2 && ./configure --prefix=/opt/check-0.15.2 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # ln -sf /opt/check-0.15.2/bin/checkmk /usr/local/bin/
            # ......................................
            # Skip # rsync -av /opt/check-0.15.2/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/check-0.15.2/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/check-0.15.2/lib/pkgconfig/check.pc /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/check-0.15.2 && return 0
    else
    
        echo "[Caution] Path: ( /opt/check-0.15.2 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 构建安装(Build Install) libinput-1.25.0
# ##################################################
function Build_Install_libinput_1_25_0() {

    if [[ ! -d "/opt/libinput-1.25.0" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( libinput-1.25.0 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/libinput-1.25.0.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # * Problem: Run-time dependency libudev found: NO (tried pkgconfig and cmake)
        #            meson.build:146:0: ERROR: Dependency "libudev" not found, tried pkgconfig and cmake
        #   - Solve: 安装 "udev" 或者 "eudev", 编译 "udev" 时出错较多 (特别是找不到 'blkid'), 推荐 "eudev".
        #            Install "udev" or "eudev", Too many compilation errors in "udev" (Especially if 'blkid' cannot be found), Recommended "eudev".
        #            ...............................
        #            "udev" 这个库在 2012 到 2013 年就停止更新了, 主要原因是内核更改了设备插拔方式接口, 用 sysfs 方式。最好使用 "eudev" 替代。
        #            The "udev" library stopped updating from 2012 to 2013, mainly because the kernel changed the device plugging method interface to use the sysfs method. It is best to use "eudev" instead.
        # ..........................................
        # *  Option: -Dlibwacom=false 这个选项的值可以为 false, 因为编译平台不是平板电脑的话, 实用意义不大, 特别是发行版系统的 glib 都封装在内核中, 容易出现 No package 'glib-2.0' found 的错误。
        cd $STORAGE/libinput-1.25.0 && meson build/ --prefix=/opt/libinput-1.25.0 \
                                                    --pkg-config-path=/opt/lib/pkgconfig && \
                                                    STEP_BUILDED=1
        
        # ------------------------------------------
        cd $STORAGE/libinput-1.25.0 && ninja -C build/ install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            # Skip # if [[ ! -d "/usr/local/libexec" ]]; then mkdir /usr/local/libexec; fi
            # ......................................
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # ln -sf /opt/libinput-1.25.0/bin/libinput /usr/local/bin/
            # ......................................
            # Skip # rsync -av /opt/libinput-1.25.0/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/libinput-1.25.0/lib/ /usr/local/lib/
            # ......................................
            # Skip # rsync -av /opt/libinput-1.25.0/libexec/ /usr/local/libexec/
            # ......................................
            cp -f /opt/libinput-1.25.0/lib/pkgconfig/libinput.pc /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/libinput-1.25.0 && return 0
    else
    
        echo "[Caution] Path: ( /opt/libinput-1.25.0 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) libwebp-1.3.1
# ##################################################
function Compile_Install_libwebp_1_3_1() {

    if [[ ! -d "/opt/libwebp-1.3.1" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( libwebp-1.3.1 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/libwebp-1.3.1.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # *  Option: --enable-swap-16bit-csp: This switch enables byte swap for 16 bit colorspaces.
        #                                     此选项启用 16 位颜色空间的字节交换。
        # *  Option: --disable-static: This switch prevents installation of static versions of the libraries.
        #                              此选项可防止安装库的静态版本。
        cd $STORAGE/libwebp-1.3.1 && ./configure --prefix=/opt/libwebp-1.3.1 \
                                                 --enable-libwebpmux     \
                                                 --enable-libwebpdemux   \
                                                 --enable-libwebpdecoder \
                                                 --enable-libwebpextras  \
                                                 --enable-swap-16bit-csp \
                                                 --disable-static && \
                                                 STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # ln -sf /opt/libwebp-1.3.1/bin/* /usr/local/bin/
            # ......................................
            # Skip # rsync -av /opt/libwebp-1.3.1/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/libwebp-1.3.1/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/libwebp-1.3.1/lib/pkgconfig/*.pc /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/libwebp-1.3.1 && return 0
    else
    
        echo "[Caution] Path: ( /opt/libwebp-1.3.1 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 构建安装(Build Install) seatd-0.8.0
# ##################################################
function Build_Install_seatd_0_8_0() {

    # seatd-0.8.0 Provide: libseat.so (Link From libseat.so.1)
    # seatd-0.8.0 Provide: libseat.so.1

    if [[ ! -d "/opt/seatd-0.8.0" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( seatd-0.8.0 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/seatd-0.8.0.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/seatd-0.8.0 && meson build/ --prefix=/opt/seatd-0.8.0 && STEP_BUILDED=1
        
        # ------------------------------------------
        cd $STORAGE/seatd-0.8.0 && ninja -C build/ install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # ln -sf /opt/seatd-0.8.0/bin/seatd        /usr/local/bin/
            # Skip # ln -sf /opt/seatd-0.8.0/bin/seatd-launch /usr/local/bin/
            # ......................................
            # Skip # rsync -av /opt/seatd-0.8.0/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/seatd-0.8.0/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/seatd-0.8.0/lib/pkgconfig/libseat.pc /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/seatd-0.8.0 && return 0
    else
    
        echo "[Caution] Path: ( /opt/seatd-0.8.0 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 构建安装(Build Install) Little-CMS-2.14
# ##################################################
function Build_Install_Little_CMS_2_14() {

    # lcms2-2.14 Provide: liblcms2.so (Link From liblcms2.so.2.0.13)
    # lcms2-2.14 Provide: liblcms2.so.2 (Link From liblcms2.so.2.0.13)
    # lcms2-2.14 Provide: liblcms2.so.2.0.13

    if [[ ! -d "/opt/lcms2-2.14" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( lcms2-2.14 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/lcms2-2.14.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # Apply the upstream fix for an issue breaking colord:
        # 为一个崩溃问题(损坏)的颜色数据应用此上游修复:
        # sed '/BufferSize < TagSize/,+1 s/goto Error/TagSize = BufferSize/' \
        #     -i src/cmsio0.c
        
        # ------------------------------------------
        cd $STORAGE/lcms2-2.14 && meson build/ --prefix=/opt/lcms2-2.14 \
                                               --pkg-config-path=/opt/lib/pkgconfig && \
                                               STEP_BUILDED=1
        
        # ------------------------------------------
        cd $STORAGE/lcms2-2.14 && ninja -C build/ install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # rsync -av /opt/lcms2-2.14/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/lcms2-2.14/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/lcms2-2.14/lib/pkgconfig/lcms2.pc /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/lcms2-2.14 && return 0
    else
    
        echo "[Caution] Path: ( /opt/lcms2-2.14 ) Already Exists."
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

# Function: 构建安装(Build Install) Pipewire-0.3.77
# ##################################################
function Build_Install_Pipewire_0_3_77() {

    if [[ ! -d "/opt/pipewire-0.3.77" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( pipewire-0.3.77 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/pipewire-0.3.77.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # *  Option: --buildtype=release: Specify a buildtype suitable for stable releases of the package, as the default may produce unoptimized binaries.
        #                                 指定一个适用于包的稳定版本的构建类型, 因为默认情况下可能会生成未优化的二进制文件。
        # ..........................................
        # *  Option: -Dsession-managers=[]: This switch allows to specify the session managers to build as subprojects.
        #                                   Since the recommended session manager ( WirePlumber) is available as a standalone project, don't specify anything here.
        #                                   This prevents downloading external dependencies during the meson step.
        #                                   此选项允许指定要作为子项目构建的会话管理器。
        #                                   由于推荐的会话管理器 (WirePlumber) 是作为一个独立项目提供的, 因此不要在此处指定任何内容。
        #                                   这可以防止在 Meson 步骤期间下载外部依赖项。
        # ..........................................
        # *  Option: -Ddocs=true: This switch enables the generation of HTML documentation. The optional dependencies for documentation need to be installed for this to work.
        #                         此选项允许生成 HTML 文档。需要安装文档的可选依赖项才能正常工作。
        # ..........................................
        # *  Option: -Dman=true: This switch enables the generation of manual pages. The optional dependencies for documentation need to be installed for this to work.
        #                        此选项允许生成手册页面。需要安装文档的可选依赖项才能正常工作。
        # ..........................................
        # *  Option: -Dffmpeg=enabled: This switch enables using ffmpeg for audio conversion as a SPA backend.
        #                              此开关允许使用 ffmpeg 作为 SPA 后端进行音频转换。
        # ..........................................
        # * Problem: [55/815] Compiling C object spa/plugins/avb/libspa-avb.so.p/avb-pcm.c.o
        #            FAILED: spa/plugins/avb/libspa-avb.so.p/avb-pcm.c.o
        #            ......
        #            ../spa/plugins/avb/avb-pcm.c: In function ‘setup_socket’:
        #            ../spa/plugins/avb/avb-pcm.c:560:22: error: storage size of ‘txtime_cfg’ isn’t known
        #               struct sock_txtime txtime_cfg;
        #                                  ^~~~~~~~~~
        #            ../spa/plugins/avb/avb-pcm.c:572:36: error: ‘SO_TXTIME’ undeclared (first use in this function); did you mean ‘SI_TIMER’?
        #               res = setsockopt(fd, SOL_SOCKET, SO_TXTIME, &txtime_cfg,
        #                                                ^~~~~~~~~
        #                                                SI_TIMER
        #            ......
        #            ../spa/plugins/avb/avb-pcm.c: In function ‘setup_msg’:
        #            ../spa/plugins/avb/avb-pcm.c:658:27: error: ‘SCM_TXTIME’ undeclared (first use in this function); did you mean ‘LC_TIME’?
        #              state->cmsg->cmsg_type = SCM_TXTIME;
        #                                       ^~~~~~~~~~
        #                                       LC_TIME
        #            [57/815] Compiling C object spa/plugins/avb/libspa-avb.so.p/avb-pcm-source.c.o
        #            ninja: build stopped: subcommand failed.
        #   - Solve: Linux 内核版本问题 (多半是过低)。
        #            修复1. 在 /usr/include/linux/net_tstamp.h 中加入 (可参照适用的系统 Include 文件 Suitable System Include Reference):
        #            
        #            +/*
        #            + * SO_TXTIME gets a struct sock_txtime with flags being an integer bit
        #            + * field comprised of these values.
        #            + */
        #            +enum txtime_flags {
        #            +    SOF_TXTIME_DEADLINE_MODE = (1 << 0),
        #            +    SOF_TXTIME_REPORT_ERRORS = (1 << 1),
        #            +    SOF_TXTIME_FLAGS_LAST = SOF_TXTIME_REPORT_ERRORS,
        #            +    SOF_TXTIME_FLAGS_MASK = (SOF_TXTIME_FLAGS_LAST - 1) |
        #            +                 SOF_TXTIME_FLAGS_LAST
        #            +};
        #            +
        #            +struct sock_txtime {
        #            +    __kernel_clockid_t  clockid;/* reference clockid */
        #            +    __u32           flags;  /* as defined by enum txtime_flags */
        #            +};
        #             
        #             #endif /* _NET_TIMESTAMPING_H */
        #
        #            修复2. /usr/include/asm-generic/socket.h 中加入 (可参照适用的系统 Include 文件 Suitable System Include Reference):
        #
        #            +#define SO_TXTIME       61
        #            +#define SCM_TXTIME      SO_TXTIME
        #             
        #             #endif /* __ASM_GENERIC_SOCKET_H */
        # ..........................................
        # * Problem: [527/815] Compiling C object src/tools/pw-cli.p/pw-cli.c.o
        #            FAILED: src/tools/pw-cli.p/pw-cli.c.o
        #            ......
        #            In file included from /opt/readline-8.2/include/readline/readline.h:36:0,
        #                             from ../src/tools/pw-cli.c:19:
        #            /opt/readline-8.2/include/readline/rltypedefs.h:35:1: error: function declaration isn’t a prototype [-Werror=strict-prototypes]
        #             typedef int Function () __attribute__((deprecated));
        #             ^~~~~~~
        #            ......
        #            In file included from ../src/tools/pw-cli.c:19:0:
        #            /opt/readline-8.2/include/readline/readline.h:410:1: error: function declaration isn’t a prototype [-Werror=strict-prototypes]
        #             extern int rl_message ();
        #             ^~~~~~
        #            cc1: some warnings being treated as errors
        #            [529/815] Compiling C object src/modules/libfilter_chain_sse.a.p/module-filter-chain_pffft.c.o
        #            ninja: build stopped: subcommand failed.
        #   - Solve: 暂未找到解决方法, 只能在 Meson 构建的时候添加 -Dreadline=disabled 来避免使用 readline 的函数。
        cd $STORAGE/pipewire-0.3.77 && meson build/ --prefix=/opt/pipewire-0.3.77 \
                                                    --buildtype=release \
                                                    --pkg-config-path=/opt/lib/pkgconfig \
                                                    -Dsession-managers="[]" \
                                                    -Dreadline=disabled && \
                                                    STEP_BUILDED=1
        
        # ------------------------------------------
        cd $STORAGE/pipewire-0.3.77 && ninja -C build/ install && STEP_INSTALLED=1
        
        # ------------------------------------------
        # If upgrading from an earlier release of Pipewire, it's needed to remove any old binary executables that interfere with the installation. As the root user:
        # 如果从早期版本的 Pipewire 升级, 则需要删除任何干扰安装的旧二进制可执行文件。作为 root 用户:
        # rm -vf /usr/bin/pipewire-*
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # ln -sf /opt/pipewire-0.3.77/bin/* /usr/local/bin/
            # ......................................
            # Skip # rsync -av /opt/pipewire-0.3.77/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/pipewire-0.3.77/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/pipewire-0.3.77/lib/pkgconfig/libpipewire-0.3.pc /opt/lib/pkgconfig/
            cp -f /opt/pipewire-0.3.77/lib/pkgconfig/libspa-0.2.pc      /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/pipewire-0.3.77 && return 0
    else
    
        echo "[Caution] Path: ( /opt/pipewire-0.3.77 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ################################## Weston (Base Wayland Protocol) ##################################

# Function: 构建安装(Build Install) Weston-13.0.0
# ##################################################
function Build_Install_Weston_13_0_0() {

    # Weston 是一个基于 Wayland 协议的显示服务器, 它实现了 Wayland 协议中定义的各种功能, 并提供了一个完整的图形显示环境。
    # Weston 提供了窗口管理, 显示布局, 输入处理, 渲染管道等功能, 可以作为一个完整的图形显示系统使用。

    if [[ ! -d "/opt/weston-13.0.0" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( Weston-13.0.0 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -xvJf $STORAGE/weston-13.0.0.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        rm /usr/local/include/weston_compile_function.h
        # ..........................................
        touch /usr/local/include/weston_compile_function.h
        echo "#include<sys/syscall.h>"                          >> /usr/local/include/weston_compile_function.h
        echo ""                                                 >> /usr/local/include/weston_compile_function.h
        echo "#ifndef SYS_gettid"                               >> /usr/local/include/weston_compile_function.h
        echo "#error \"SYS_gettid unavailable on this system\"" >> /usr/local/include/weston_compile_function.h
        echo "#endif"                                           >> /usr/local/include/weston_compile_function.h
        echo ""                                                 >> /usr/local/include/weston_compile_function.h
        echo "pid_t gettid() {return syscall(SYS_gettid);}"     >> /usr/local/include/weston_compile_function.h
        # ..........................................
        sed -i "50i \#include \<weston_compile_function\.h\>" $STORAGE/weston-13.0.0/libweston/backend-rdp/rdp.c
        
        # ------------------------------------------
        # *  Option: -Dbackend-rdp=false: 可选参数 (若选项值为 true 则需要 FreeRDP2)。
        # ..........................................
        # *  Option: -Dbackend-vnc=false: 可选参数 (若选项值为 true 则需要 Neat-VNC)。
        # ..........................................
        # *  Option: -Dxwayland=false: 可选参数 (若选项值为 true 则需要 libXcursor)。
        # ..........................................
        # *  Option: -Dsystemd=false: 可选参数 (若选项值为 true 则需要 Systemd)。
        # ..........................................
        # *  Option: -Dremoting=false: 可选参数 (若选项值为 true 则需要 GStreamer1.0)。
        cd $STORAGE/weston-13.0.0 && meson build/ --prefix=/opt/weston-13.0.0 \
                                                  --pkg-config-path=/opt/lib/pkgconfig \
                                                  -Dbackend-rdp=true \
                                                  -Dbackend-vnc=true \
                                                  -Dxwayland=true \
                                                  -Dsystemd=true \
                                                  -Dremoting=true && \
                                                  STEP_BUILDED=1
        
        # ------------------------------------------
        # * Problem: libweston/backend-rdp/rdp-backend.so.p/rdp.c.o：in function 'rdp_backend_create'：
        #            /home/goufeng/weston-13.0.0/build/../libweston/backend-rdp/rdp.c:1813：undefined reference to 'gettid'
        #            libweston/backend-rdp/rdp-backend.so.p/rdputil.c.o：in function 'assert_compositor_thread'：
        #            /home/goufeng/weston-13.0.0/build/../libweston/backend-rdp/rdputil.c:82：undefined reference to 'gettid'
        #            libweston/backend-rdp/rdp-backend.so.p/rdputil.c.o：in function 'assert_not_compositor_thread'：
        #            /home/goufeng/weston-13.0.0/build/../libweston/backend-rdp/rdputil.c:88：undefined reference to 'gettid'
        #            collect2: error: ld returned 1 exit status
        #            [205/570] Compiling C object libweston/backend-wayland/wayland-backend.so.p/meson-generated_.._.._.._protocol_presentation-time-protocol.c.o
        #            ninja: build stopped: subcommand failed.
        # * - Solve: 解决方法 1. 自己在系统外层封装 gettid() 函数。
        #                因为 gettid() 是 Linux 系统的函数, 用于获取当前线程的 ID, 该函数在标准 C 库中并不存在。
        #                因此把里面实现函数复制出来, 写到自己的程序里即可:
        #                    /* 包含此头文件 */
        #                    #include<sys/syscall.h>
        #                    
        #                    #ifndef SYS_gettid
        #                    #error "SYS_gettid unavailable on this system"
        #                    #endif
        #                    
        #                    pid_t gettid() {return syscall(SYS_gettid);}
        #                或者:
        #                    /* 包含此头文件 */
        #                    #include <linux/unistd.h>
        #                    
        #                    #ifndef __NR_gettid
        #                    #error "__NR_gettid unavailable on this system"
        #                    #endif
        #                    
        #                    pid_t gettid(void) {return syscall(__NR_gettid);}
        #            解决方法 2. 在编译时链接 pthread 库。
        #                在编译命令中加入 -pthread 选项, 例如: "gcc -pthread example.c -o example"。
        #                如果还是出错, 尝试在编译命令中加入 -lpthread 选项, 例如: "gcc example.c -o example -lpthread"。
        # ..........................................
        cd $STORAGE/weston-13.0.0 && ninja -C build/ install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            # Skip # if [[ ! -d "/usr/local/libexec" ]]; then mkdir /usr/local/libexec; fi
            # ......................................
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            ln -sf /opt/weston-13.0.0/bin/* /usr/local/bin/
            # ......................................
            # Skip # rsync -av /opt/weston-13.0.0/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/weston-13.0.0/lib/ /usr/local/lib/
            # ......................................
            # Skip # rsync -av /opt/weston-13.0.0/libexec/ /usr/local/libexec/
            # ......................................
            cp -f /opt/weston-13.0.0/lib/pkgconfig/libweston-13.pc /opt/lib/pkgconfig/
            cp -f /opt/weston-13.0.0/lib/pkgconfig/weston.pc       /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/weston-13.0.0 && return 0
    else
    
        echo "[Caution] Path: ( /opt/weston-13.0.0 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

function main() {

    # ----------- Compilation Environment ----------
    # 编译 libusb 时需要引入 eudev 的 include 头文件。
    # 编译 Weston 时需要引入 Linux-PAM 的 include 头文件。
    export C_INCLUDE_PATH=/opt/eudev-3.2.14/include:/opt/Linux-PAM-1.5.2/include
    export CPLUS_INCLUDE_PATH=/opt/eudev-3.2.14/include:/opt/Linux-PAM-1.5.2/include
    # ..............................................
    # 编译 libgudev 时需要引入 glib 的 lib 库文件。
    # 编译 libinput 时需要引入 libjpeg-turbo 的 lib 库文件
    # >>>>>>>>>>>>>>>>>>>>>>>> libevdev 的 lib 库文件。
    # >>>>>>>>>>>>>>>>>>>>>>>> Fribidi 的 lib 库文件。
    # 编译 Weston 时需要引入 Linux-PAM 的 lib 库文件。
    # >>>>>>>>>>>>>>>>>>>>>>>> libwacom 的 lib 库文件。
    # >>>>>>>>>>>>>>>>>>>>>>>> libdrm 的 lib 库文件。
    export LIBRARY_PATH=/opt/sandbox-glib/lib:/opt/libjpeg-turbo-3.0.0/lib:/opt/libevdev-1.11.0/lib:/opt/fribidi-1.0.13/lib:/opt/Linux-PAM-1.5.2/lib:/opt/libwacom-2.10.0/lib:/opt/libdrm-2.4.120/lib
    export LD_LIBRARY_PATH=/opt/sandbox-glib/lib:/opt/libjpeg-turbo-3.0.0/lib:/opt/libevdev-1.11.0/lib:/opt/fribidi-1.0.13/lib:/opt/Linux-PAM-1.5.2/lib:/opt/libwacom-2.10.0/lib:/opt/libdrm-2.4.120/lib
    # ..............................................
    # 编译 libgudev 时需要引入 glib 的 bin 二进制文件。
    export PATH=$PATH:/opt/sandbox-glib/bin
    
    # ----------------------------------------------
    # 可能需要修改 Linux 系统内核头文件 /usr/include/linux/net_tstamp.h, 详见 Pipewire-0.3.77 编译过程问题处理。
    # 可能需要修改 Linux 系统内核头文件 /usr/include/asm-generic/socket.h, 详见 Pipewire-0.3.77 编译过程问题处理。

    # -------------- X11 - libXcursor --------------
    Compile_Install_xcb_util_0_4_1
    Compile_Install_xcb_util_image_0_4_1
    Compile_Install_xcb_util_renderutil_0_3_10
    Compile_Install_xcb_util_cursor_0_1_4
    Compile_Install_libXcursor_1_2_0
    # ------ libinput Dep: libwacom (Optional) -----
    Compile_Install_eudev_3_2_14
    Compile_Install_mtdev_1_1_6
    Compile_Install_libevdev_1_11_0
    Build_Install_libgudev_238
    Build_Install_pyudev_0_24_1_by_Python3
    Build_Install_libevdev_0_11_by_Python3
    Pip_Install_tomli_2_0_1_by_Python3
    Pip_Install_iniconfig_2_0_0_by_Python3
    Pip_Install_exceptiongroup_1_2_0_by_Python3
    Build_Install_pluggy_1_4_0_by_Python3
    Pip_Install_Packaging_23_2_by_Python3
    Pip_Install_pytest_8_1_0_by_Python3
    Build_Install_libwacom_2_10_0
    # - Weston (Base Wayland Proto) Dep: Linux-PAM -
    Compile_Install_Linxu_PAM_1_5_2
    # -- Weston (Base Wayland Protocol) Dependency -
    Build_Install_libxkbcommon_1_6_0
    Compile_Install_check_0_15_2
    Build_Install_libinput_1_25_0
    Compile_Install_libwebp_1_3_1
    Build_Install_seatd_0_8_0
    Build_Install_Little_CMS_2_14
    Build_Install_libva_2_19_0
    Build_Install_Pipewire_0_3_77
    # ------- Weston (Base Wayland Protocol) -------
    Build_Install_Weston_13_0_0
}

main
```

## 总结

以上就是关于 Linux运维 Bash脚本 构建安装Weston-13.0.0 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
