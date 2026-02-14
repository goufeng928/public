# 文章_Linux运维_Bash脚本_编译安装eudev和libgudev_GF_2024-03-08

Bash (Bourne Again Shell) 是一个解释器，负责处理 Unix 系统命令行上的命令。它是由 Brian Fox 编写的免费软件，并于 1989 年发布的免费软件，作为 Sh (Bourne Shell) 的替代品。

您可以在 Linux 和 MacOS 机器上使用 Bash，甚至可以通过适用于 Linux 的 Windows 子系统在 Windows 10 机器上使用。

## 使用方法

* 下载源码包:

eudev-3.2.10.tar.gz -> (udev-243)

eudev-3.2.14.tar.gz -> (udev-251)

libgudev-238.tar.xz
  
* 放于指定路径:

这里 Bash Shell 脚本的全局变量 STORAGE 指定的存放源码包的路径 ==/home/goufeng== 可进行修改。
  
* 执行 Bash Shell 脚本:

输入 ==/[路径名]/[脚本名].sh== 即可进行自动编译部署，过程中提示输入 **(y/n)** 输入 **y** 则进行下一步，这样分阶段确认的原因是为了确保能够看到上一个源码编译结果中可能的错误和提示。

## 完整脚本

```shell
#! /bin/bash
# Create By GF 2024-03-08 23:41

# --------------------------------------------------
# Install First: 
# * GNU-Tools (Contains: pkg-config, m4, autoconf, automake, libtool, gettext, flex, bison, libiconv, make)
# * Python == 3.x.x
# * Meson
# * Ninja

# --------------------- eudev ----------------------
# Need File: eudev-3.2.10.tar.gz -> (udev-243)
# Need File: eudev-3.2.14.tar.gz -> (udev-251)
# -------------------- libgudev --------------------
# Need File: libgudev-238.tar.xz

# ##################################################
# Recommended Pairing (Mate):
# * eudev-3.2.14 (udev-251) & libgudev-238

# ##################################################
STORAGE=/home/goufeng

# ############################################## eudev ###############################################

# Function: 编译安装(Compile Install) eudev-3.2.10
# ##################################################
function Compile_Install_eudev_3_2_10() {

    # Attention: may conflict with the original "udev" in the system.
    # 注意: 可能与系统原有的 "udev" 冲突。

    # eudev 提供针对内核提供的 udev 设备管理服务的函数库。
    # udev 是 Linux 2.6 内核的设备管理器。
    # udev 它在 /dev 目录下动态地 创建/移除 设备节点, 用于在系统中传递解决方案的有关设备信息, 以及在出现设备事件 (如删除、插入设备) 时触发相应的操作。

    if [[ ! -d "/opt/eudev-3.2.10" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( eudev-3.2.10 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/eudev-3.2.10.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/eudev-3.2.10 && ./configure --prefix=/opt/eudev-3.2.10 && STEP_BUILDED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # Skip # if [[ ! -d "/usr/local/sbin" ]]; then mkdir /usr/local/sbin; fi
            # ......................................
            # Skip # ln -sf /opt/eudev-3.2.10/bin/udevadm /usr/local/bin/
            # Skip # ln -sf /opt/eudev-3.2.10/bin/udevadm /usr/local/sbin/udevadm
            # ......................................
            # Skip # ln -sf /opt/eudev-3.2.10/sbin/udevd /usr/local/sbin/
            # ......................................
            # Skip # rsync -av /opt/eudev-3.2.10/include/ /usr/local/include/
            # Skip # rsync -av /opt/eudev-3.2.10/lib/     /usr/local/lib/
            # ......................................
            cp -f /opt/eudev-3.2.10/lib/pkgconfig/libudev.pc /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/eudev-3.2.10 && return 0
    else
    
        echo "[Caution] Path: ( /opt/eudev-3.2.10 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

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
            # Skip # rsync -av /opt/eudev-3.2.14/lib/     /usr/local/lib/
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

# ############################################# libgudev #############################################

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
        # Skip # export PATH=$PATH:/opt/glib-2.78.4/bin
        # Skip # export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/pcre2-10.43/lib
        
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
            # Skip # rsync -av /opt/libgudev-238/lib/     /usr/local/lib/
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

function main() {

    # ------------------- eudev --------------------
    #Compile_Install_eudev_3_2_10 # -> (udev-243)
    Compile_Install_eudev_3_2_14  # -> (udev-251)
    # ------------------ libgudev ------------------
    Build_Install_libgudev_238
}

main
```

## 总结

以上就是关于 Linux运维 Bash脚本 编译安装eudev和libgudev 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
