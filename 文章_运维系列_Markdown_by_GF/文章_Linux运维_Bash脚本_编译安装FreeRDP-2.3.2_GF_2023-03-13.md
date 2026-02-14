# 文章_Linux运维_Bash脚本_编译安装FreeRDP-2.3.2_GF_2023-03-13

Bash (Bourne Again Shell) 是一个解释器，负责处理 Unix 系统命令行上的命令。它是由 Brian Fox 编写的免费软件，并于 1989 年发布的免费软件，作为 Sh (Bourne Shell) 的替代品。

您可以在 Linux 和 MacOS 机器上使用 Bash，甚至可以通过适用于 Linux 的 Windows 子系统在 Windows 10 机器上使用。

## 使用方法

* 下载源码包:

eudev-3.2.14.tar.gz

libusb-1.0.27.tar.bz2

freerdp-2.3.2.tar.gz
  
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
# * CMake >= 3.5.0
# * FFmpeg == 3.x.x

# ------------------- Dependency -------------------
# Need File: eudev-3.2.14.tar.gz
# Need File: libusb-1.0.27.tar.bz2
# -------------------- FreeRDP ---------------------
# Need File: freerdp-2.3.2.tar.gz

# ##################################################
# Recommended Optional Installation
# * GnuTLS-3.7.0 (GnuTLS是一个安全的通信库, 实现 SSL, TLS 和 DTLS 协议及其周围的技术。它提供了用于访问安全通信协议的简单 C语言 应用程序编程接口 (API), 以及用于解析和编写 X.509, PKCS 和其他所需结构的API。)

# ##################################################
STORAGE=/home/goufeng

# ############################################ Dependency ############################################

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

# Function: 编译安装(Compile Install) libusb-1.0.27
# ##################################################
function Compile_Install_libusb_1_0_27() {

    # Configuring Libusb
    #     To access raw USB devices (those not treated as a disk by the mass-storage driver), appropriate support must be available in the kernel. Check your kernel configuration:
    #     
    #     Device Drivers --->
    #       [*] USB support --->                                             [USB_SUPPORT]
    #         <*/M>   Support for Host-side USB                                      [USB]
    #         [*]     PCI based USB host interface                               [USB_PCI]
    #         # These are most common USB controller drivers for PC-like systems.
    #         # For modern systems often [USB_XHCI_HCD] is the only one needed
    #         # even if the system has USB 2.0 ports:
    #         < /*/M> xHCI HCD (USB 3.0) support                            [USB_XHCI_HCD]
    #         < /*/M> EHCI HCD (USB 2.0) support                            [USB_EHCI_HCD]
    #         < /*/M> OHCI HCD (USB 1.1) support                            [USB_OHCI_HCD]
    #     For more details on setting up USB devices, see the section called “USB Device Issues”.

    if [[ ! -d "/opt/libusb-1.0.27" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( libusb-1.0.27 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -jxvf $STORAGE/libusb-1.0.27.tar.bz2 && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/libusb-1.0.27 && ./configure --prefix=/opt/libusb-1.0.27 \
                                                 --disable-static \
                                                 PKG_CONFIG_PATH="/opt/lib/pkgconfig" && \
                                                 STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # rsync -av /opt/libusb-1.0.27/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/libusb-1.0.27/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/libusb-1.0.27/lib/pkgconfig/libusb-1.0.pc /opt/lib/pkgconfig/
        fi
        
        # ------------------------------------------
        # If Doxygen is installed and you wish to build the API documentation, issue the following commands:
        # 如果安装了 Doxygen, 并且您希望构建 API 文档, 请发出以下命令:
        #     pushd doc                &&
        #       doxygen -u doxygen.cfg &&
        #       make docs              &&
        #     popd
        # ..........................................
        # This package does not come with a test suite.
        # 此软件包没有附带测试套件。
        # ..........................................
        # If you built the API documentation, install it using the following commands as the root user:
        # 如果您构建了 API 文档, 请使用以下命令作为 root 用户进行安装:
        #     install -v -d -m755 /usr/share/doc/libusb-1.0.27/apidocs &&
        #     install -v -m644    doc/api-1.0/* \
        #                         /usr/share/doc/libusb-1.0.27/apidocs

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/libusb-1.0.27 && return 0
    else
    
        echo "[Caution] Path: ( /opt/libusb-1.0.27 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ############################################# FreeRDP ##############################################

# Function: 构建安装(Build Install) FreeRDP-2.3.2
# ##################################################
function Build_Install_FreeRDP_2_3_2() {

    # FreeRDP 在编译时候默认没有打开 FreeRDP Server 需要使 WITH_SERVER 的值是 ON:
    #     -DWITH_SERVER=ON
    # ..............................................
    # 小知识: Windows 下编 FreeRDP 需要在 CMakeLists.txt 增加 CMAKE_WINDOWS_VERSION 并赋值 WIN8 及以上 (String 类型值):
    #             <FreeRDP>/CMakeLists.txt
    #             if(NOT DEFINED CMAKE_WINDOWS_VERSION)
    #               set(CMAKE_WINDOWS_VERSION "WIN7")
    #             endif()
    #         CMAKE_WINDOWS_VERSION 决定了预定义宏 _WIN32_WINNT 是什么值。
    #         要是不预先设置 CMAKE_WINDOWS_VERSION, 值将是 0x0601, 此时抓屏将使用 "Mirage Driver" 技术。
    #             <FreeRDP>/server/Windows/wf_interface.h，
    #             #if _WIN32_WINNT >= 0x0602
    #             #define WITH_DXGI_1_2 1
    #             #endif
    #         Win8 或以上系统已不再支持 "Mirage Driver",用它抓屏会出异常, 必须使用 DXGI。

    if [[ ! -d "/opt/freerdp-2.3.2" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CREATED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( freerdp-2.3.2 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/freerdp-2.3.2.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        if [[ $STEP_UNZIPPED == 1 ]]; then
            sed -i "24i SET(CMAKE_INCLUDE_PATH /opt/libusb-1.0.27/include)" $STORAGE/freerdp-2.3.2/CMakeLists.txt
            sed -i "25i SET(CMAKE_LIBRARY_PATH /opt/libusb-1.0.27/lib)" $STORAGE/freerdp-2.3.2/CMakeLists.txt
        fi
        
        # ------------------------------------------
        mkdir $STORAGE/freerdp-2.3.2/build && STEP_CREATED=1
        
        # ------------------------------------------
        # * Problem: ../../libfreerdp/libfreerdp2.so.2.3.2：undefined reference to 'avcodec_register_all'
        #            collect2: error: ld returned 1 exit status
        #   - Solve: 更换 (降低) FFmpeg 版本:
        #            FFmpeg 的 avcodec_register_all() 用于注册编解码器, FFmpeg 4.0 版本以前是调用该方法, 运行期把所有编译的编解码器添加到链表。
        #            但是 FFmpeg 4.0 版本以后, 改为编译期自动生成编解码数组, 还有解析器数组。
        #            在 API Changes 文档中有说明, FFmpeg 4.0 版本以后, avcodec_register_all() 等方法已经过时, 添加 av_codec_iterate(), av_parser_iterate() 来迭代遍历, API 改动如下:
        #                2018-02-06 - 36c85d6e77 - lavc 58.10.100 - avcodec.h
        #                  Deprecate use of avcodec_register(), avcodec_register_all(),
        #                  av_codec_next(), av_register_codec_parser(), and av_parser_next().
        #                  Add av_codec_iterate() and av_parser_iterate().
        cd $STORAGE/freerdp-2.3.2/build && cmake -G "Unix Makefiles" \
                                                 -DCMAKE_INSTALL_PREFIX=/opt/freerdp-2.3.2 \
                                                 -DCMAKE_BUILD_TYPE=Release \
                                                 -DWITH_SERVER=ON \
                                                 ../ && STEP_BUILDED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            ln -sf /opt/freerdp-2.3.2/bin/* /usr/local/bin/
            # ......................................
            # Skip # rsync -av /opt/freerdp-2.3.2/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/freerdp-2.3.2/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/freerdp-2.3.2/lib/pkgconfig/*.pc /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/freerdp-2.3.2 && return 0
    else
    
        echo "[Caution] Path: ( /opt/freerdp-2.3.2 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

function main() {

    # ----------- Compilation Environment ----------
    # 编译 libusb 时需要引入 eudev 的 include 头文件。
    export C_INCLUDE_PATH=/opt/eudev-3.2.14/include
    export CPLUS_INCLUDE_PATH=/opt/eudev-3.2.14/include
    # ..............................................
    # 编译 libusb 时需要引入 eudev 的 lib 库文件。
    export LIBRARY_PATH=/opt/eudev-3.2.14/lib
    export LD_LIBRARY_PATH=/opt/eudev-3.2.14/lib
    # ..............................................
    # 编译 FreeRDP2 时需要引入 PKG_CONFIG_PATH 环境变量。
    export PKG_CONFIG_PATH=/opt/lib/pkgconfig

    # ----------------- Dependency -----------------
    Compile_Install_eudev_3_2_14
    Compile_Install_libusb_1_0_27
    # ------------------ FreeRDP -------------------
    Build_Install_FreeRDP_2_3_2
}

main
```

## 总结

以上就是关于 Linux运维 Bash脚本 编译安装FreeRDP-2.3.2 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
