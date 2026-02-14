# 文章_Linux运维_Bash脚本_编译安装FFmpeg-6.0_GF_2023-03-11

Bash (Bourne Again Shell) 是一个解释器，负责处理 Unix 系统命令行上的命令。它是由 Brian Fox 编写的免费软件，并于 1989 年发布的免费软件，作为 Sh (Bourne Shell) 的替代品。

您可以在 Linux 和 MacOS 机器上使用 Bash，甚至可以通过适用于 Linux 的 Windows 子系统在 Windows 10 机器上使用。

## 使用方法

* 下载源码包:

yasm-1.3.0.tar.gz

nasm-2.16.01.tar.xz

libaom-3.6.1.tar.gz

libass-0.17.1.tar.xz

fdk-aac-2.0.2.tar.gz

lame-3.100.tar.gz

opus-1.3.1.tar.gz

libogg-1.3.5.tar.xz

libtheora-1.1.1.tar.xz

libvorbis-1.3.7.tar.xz

libvpx-1.13.0.tar.gz

x264-20230215.tar.xz

x265-20230215.tar.xz

ffmpeg-6.0-chromium_method-1.patch

ffmpeg-6.0-binutils_2.41-1.patch

ffmpeg-6.0.tar.gz
  
* 放于指定路径:

这里 Bash Shell 脚本的全局变量 STORAGE 指定的存放源码包的路径 ==/home/goufeng== 可进行修改。
  
* 执行 Bash Shell 脚本:

输入 ==/[路径名]/[脚本名].sh== 即可进行自动编译部署，过程中提示输入 **(y/n)** 输入 **y** 则进行下一步，这样分阶段确认的原因是为了确保能够看到上一个源码编译结果中可能的错误和提示。

## 完整脚本

```shell
#! /bin/bash
# Create By GF 2024-03-11 01:22

# --------------------------------------------------
# Install First: 
# * GNU-Tools (Contains: pkg-config, m4, autoconf, automake, libtool, gettext, flex, bison, libiconv, make)
# * CMake >= 3.14.0
# * Pango == 1.51.x (Contains: Fribidi, FreeType, Fontconfig)

# ------------------- Dependency -------------------
# Need File: yasm-1.3.0.tar.gz
# Need File: nasm-2.16.01.tar.xz
# Need File: libaom-3.6.1.tar.gz
# Need File: libass-0.17.1.tar.xz
# Need File: fdk-aac-2.0.2.tar.gz
# Need File: lame-3.100.tar.gz
# Need File: opus-1.3.1.tar.gz
# Need File: libogg-1.3.5.tar.xz
# Need File: libtheora-1.1.1.tar.xz
# Need File: libvorbis-1.3.7.tar.xz
# Need File: libvpx-1.13.0.tar.gz
# Need File: x264-20230215.tar.xz
# Need File: x265-20230215.tar.xz
# ------------------ FFmpeg - 6.0 ------------------
# Need File: ffmpeg-6.0-chromium_method-1.patch
# Need File: ffmpeg-6.0-binutils_2.41-1.patch
# Need File: ffmpeg-6.0.tar.gz

# ##################################################
STORAGE=/home/goufeng

# ############################################ Dependency ############################################

# Function: 编译安装(Compile Install) yasm-1.3.0
# ##################################################
function Compile_Install_yasm_1_3_0() {

    if [[ ! -d "/opt/yasm-1.3.0" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( yasm-1.3.0 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/yasm-1.3.0.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # * Explain: sed -i 's#) ytasm.*#)#' Makefile.in: This sed prevents it compiling 2 programs (vsyasm and ytasm) that are only of use on Microsoft Windows.
        #                                                 此 sed 阻止它编译仅在 Microsoft Windows 上使用的 2 个程序 (vsyasm 和 ytasm)。
        if [[ $STEP_UNZIPPED == 1 ]]; then
            sed -i 's#) ytasm.*#)#' $STORAGE/yasm-1.3.0/Makefile.in
        fi
        
        # ------------------------------------------
        cd $STORAGE/yasm-1.3.0 && ./configure --prefix=/opt/yasm-1.3.0 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            # Default None .pc (Pkg-Config) File.
            # ......................................
            ln -sf /opt/yasm-1.3.0/bin/yasm /usr/local/bin/
            # ......................................
            rsync -av /opt/yasm-1.3.0/include/ /usr/local/include/
            rsync -av /opt/yasm-1.3.0/lib/     /usr/local/lib/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/yasm-1.3.0 && return 0
    else
    
        echo "[Caution] Path: ( /opt/yasm-1.3.0 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) NASM-2.16.01
# ##################################################
function Compile_Install_NASM_2_16_01() {

    if [[ ! -d "/opt/nasm-2.16.01" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( nasm-2.16.01 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -xvJf $STORAGE/nasm-2.16.01.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/nasm-2.16.01 && ./configure --prefix=/opt/nasm-2.16.01 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            # By Default, Only Binary Files Are Available.
            # ......................................
            ln -sf /opt/nasm-2.16.01/bin/nasm    /usr/local/bin/
            ln -sf /opt/nasm-2.16.01/bin/ndisasm /usr/local/bin/
        fi
        
        # ------------------------------------------
        # If you downloaded the optional documentation, install it with the following instructions as the root user:
        # 如果下载了可选文档, 请以 root 用户身份按照以下说明进行安装:
        # install -m755 -d         /usr/share/doc/nasm-2.16.01/html  &&
        # cp -v doc/html/*.html    /usr/share/doc/nasm-2.16.01/html  &&
        # cp -v doc/*.{txt,ps,pdf} /usr/share/doc/nasm-2.16.01

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/nasm-2.16.01 && return 0
    else
    
        echo "[Caution] Path: ( /opt/nasm-2.16.01 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 构建安装(Build Install) libaom-3.6.1
# ##################################################
function Build_Install_libaom_3_6_1() {

    if [[ ! -d "/opt/libaom-3.6.1" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CREATED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( libaom-3.6.1 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/libaom-3.6.1.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        mkdir $STORAGE/libaom-3.6.1/build && STEP_CREATED=1
        
        # ------------------------------------------
        # * Default Configure Options:
        #   cmake -DCMAKE_INSTALL_PREFIX=/usr \
        #         -DCMAKE_BUILD_TYPE=Release \
        #         -DBUILD_SHARED_LIBS=1 \
        #         -DENABLE_DOCS=no \
        #         -G Ninja ..
        # ..........................................
        # To test the results, issue: ninja runtests. Note that the tests take an extremely long time to run.
        # 要测试结果, 请使用指令: "ninja runtests"。请注意, 运行这些测试需要非常长的时间。
        # ..........................................
        # *  Option:-DBUILD_SHARED_LIBS=1: This switch builds shared versions of the libraries.
        #                                  此选项构建库的共享版本。
        # ..........................................
        # *  Option:-DENABLE_DOCS=no: This switch disables building the documentation because it fails due to an incompatibility with the latest version of Doxygen-1.9.7.
        #                             由于与最新版本的 Doxygen-1.9.7 不兼容, 此开关将禁用生成文档。
        # ..........................................
        # *  Option:-DENABLE_NASM=yes: Use this switch if you have NASM-2.16.01 installed and wish to use it instead of yasm.
        #                              如果您安装了 NASM-2.16.01 并希望使用它而不是 yasm, 请使用此开关。
        cd $STORAGE/libaom-3.6.1/build && cmake -G "Ninja" \
                                                -DCMAKE_INSTALL_PREFIX=/opt/libaom-3.6.1 \
                                                -DCMAKE_BUILD_TYPE=Release \
                                                -DBUILD_SHARED_LIBS=1 \
                                                ../ && STEP_BUILDED=1
        
        # ------------------------------------------
        cd $STORAGE/libaom-3.6.1 && ninja -C build/ install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            ln -sf /opt/libaom-3.6.1/bin/aomdec /usr/local/bin/
            ln -sf /opt/libaom-3.6.1/bin/aomenc /usr/local/bin/
            # ......................................
            rsync -av /opt/libaom-3.6.1/include/ /usr/local/include/
            rsync -av /opt/libaom-3.6.1/lib/     /usr/local/lib/
            # ......................................
            cp -f /opt/libaom-3.6.1/lib/pkgconfig/aom.pc /opt/lib/pkgconfig/
        fi
        
        # ------------------------------------------
        # Now, as the root user:
        # ninja install &&
        # rm -v /usr/lib/libaom.a

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/libaom-3.6.1 && return 0
    else
    
        echo "[Caution] Path: ( /opt/libaom-3.6.1 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) libass-0.17.1
# ##################################################
function Compile_Install_libass_0_17_1() {

    if [[ ! -d "/opt/libass-0.17.1" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( libass-0.17.1 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -xvJf $STORAGE/libass-0.17.1.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/libass-0.17.1 && ./configure --prefix=/opt/libass-0.17.1 \
                                                 PKG_CONFIG_PATH="/opt/lib/pkgconfig" && \
                                                 STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            rsync -av /opt/libass-0.17.1/include/ /usr/local/include/
            rsync -av /opt/libass-0.17.1/lib/     /usr/local/lib/
            # ......................................
            cp -f /opt/libass-0.17.1/lib/pkgconfig/libass.pc /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/libass-0.17.1 && return 0
    else
    
        echo "[Caution] Path: ( /opt/libass-0.17.1 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) fdk-aac-2.0.2
# ##################################################
function Compile_Install_fdk_aac_2_0_2() {

    if [[ ! -d "/opt/fdk-aac-2.0.2" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( fdk-aac-2.0.2 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/fdk-aac-2.0.2.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/fdk-aac-2.0.2 && ./configure --prefix=/opt/fdk-aac-2.0.2 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            rsync -av /opt/fdk-aac-2.0.2/include/ /usr/local/include/
            rsync -av /opt/fdk-aac-2.0.2/lib/     /usr/local/lib/
            # ......................................
            cp -f /opt/fdk-aac-2.0.2/lib/pkgconfig/fdk-aac.pc /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/fdk-aac-2.0.2 && return 0
    else
    
        echo "[Caution] Path: ( /opt/fdk-aac-2.0.2 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) LAME-3.100
# ##################################################
function Compile_Install_LAME_3_100() {

    # lame-3.100 Provide: libmp3lame.so (Link From libmp3lame.so.0.0.0)
    # lame-3.100 Provide: libmp3lame.so.0.0.0

    if [[ ! -d "/opt/lame-3.100" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( lame-3.100 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/lame-3.100.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # *  Option: --enable-mp3rtp: This switch enables building the encode-to-RTP program.
        #                             此选项允许构建编码到 RTP 程序。
        # ..........................................
        # *  Option: --disable-static: This switch prevents installation of static versions of the libraries.
        #                              此选项可防止安装库的静态版本。
        # ..........................................
        # *  Option: --enable-nasm: Enable the use of NASM-2.16.01 to compile optimized assembly routines for 32-bit x86. This option has no effect on x86_64.
        #                           允许使用 NASM-2.16.01 为 32 位 x86 编译优化的汇编例程。此选项对 x86_64 没有影响。
        cd $STORAGE/lame-3.100 && ./configure --prefix=/opt/lame-3.100 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        # Now, as the root user:
        # make pkghtmldir=/usr/share/doc/lame-3.100 install
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            # Default None .pc (Pkg-Config) File.
            # ......................................
            ln -sf /opt/lame-3.100/bin/lame /usr/local/bin/
            # ......................................
            rsync -av /opt/lame-3.100/include/ /usr/local/include/
            rsync -av /opt/lame-3.100/lib/     /usr/local/lib/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/lame-3.100 && return 0
    else
    
        echo "[Caution] Path: ( /opt/lame-3.100 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) Opus-1.3.1
# ##################################################
function Compile_Install_Opus_1_3_1() {

    if [[ ! -d "/opt/opus-1.3.1" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( opus-1.3.1 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/opus-1.3.1.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/opus-1.3.1 && ./configure --prefix=/opt/opus-1.3.1 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            rsync -av /opt/opus-1.3.1/include/ /usr/local/include/
            rsync -av /opt/opus-1.3.1/lib/     /usr/local/lib/
            # ......................................
            cp -f /opt/opus-1.3.1/lib/pkgconfig/opus.pc /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/opus-1.3.1 && return 0
    else
    
        echo "[Caution] Path: ( /opt/opus-1.3.1 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) libogg-1.3.5
# ##################################################
function Compile_Install_libogg_1_3_5() {

    if [[ ! -d "/opt/libogg-1.3.5" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( libogg-1.3.5 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -xvJf $STORAGE/libogg-1.3.5.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/libogg-1.3.5 && ./configure --prefix=/opt/libogg-1.3.5 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            rsync -av /opt/libogg-1.3.5/include/ /usr/local/include/
            rsync -av /opt/libogg-1.3.5/lib/     /usr/local/lib/
            # ......................................
            cp -f /opt/libogg-1.3.5/lib/pkgconfig/ogg.pc /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/libogg-1.3.5 && return 0
    else
    
        echo "[Caution] Path: ( /opt/libogg-1.3.5 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) libtheora-1.1.1
# ##################################################
function Compile_Install_libtheora_1_1_1() {

    if [[ ! -d "/opt/libtheora-1.1.1" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( libtheora-1.1.1 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -xvJf $STORAGE/libtheora-1.1.1.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # * Explain: sed -i 's/png_\(sizeof\)/\1/g' examples/png2theora.c: This sed fixes build with libpng 1.6.
        #                                                                  此 sed 修复了使用 libpng 1.6 构建的问题。
        if [[ $STEP_UNZIPPED == 1 ]]; then
            # Install libtheora by running the following commands:
            sed -i 's/png_\(sizeof\)/\1/g' $STORAGE/libtheora-1.1.1/examples/png2theora.c
        fi
        
        # ------------------------------------------
        cd $STORAGE/libtheora-1.1.1 && ./configure --prefix=/opt/libtheora-1.1.1 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            rsync -av /opt/libtheora-1.1.1/include/ /usr/local/include/
            rsync -av /opt/libtheora-1.1.1/lib/     /usr/local/lib/
            # ......................................
            cp -f /opt/libtheora-1.1.1/lib/pkgconfig/theora.pc    /opt/lib/pkgconfig/
            cp -f /opt/libtheora-1.1.1/lib/pkgconfig/theoradec.pc /opt/lib/pkgconfig/
            cp -f /opt/libtheora-1.1.1/lib/pkgconfig/theoraenc.pc /opt/lib/pkgconfig/
        fi
        
        # ------------------------------------------
        # If you wish to install the examples (so that you can hack on theora), install them as the root user:
        # 如果你想安装这些示例 (这样你就可以破解 theora), 请以 root 用户的身份安装它们:
        # cd examples/.libs &&
        # for E in *; do
        #   install -v -m755 $E /usr/bin/theora_${E}
        # done

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/libtheora-1.1.1 && return 0
    else
    
        echo "[Caution] Path: ( /opt/libtheora-1.1.1 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) libvorbis-1.3.7
# ##################################################
function Compile_Install_libvorbis_1_3_7() {

    if [[ ! -d "/opt/libvorbis-1.3.7" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( libvorbis-1.3.7 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -xvJf $STORAGE/libvorbis-1.3.7.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/libvorbis-1.3.7 && ./configure --prefix=/opt/libvorbis-1.3.7 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            rsync -av /opt/libvorbis-1.3.7/include/ /usr/local/include/
            rsync -av /opt/libvorbis-1.3.7/lib/     /usr/local/lib/
            # ......................................
            cp -f /opt/libvorbis-1.3.7/lib/pkgconfig/vorbis.pc     /opt/lib/pkgconfig/
            cp -f /opt/libvorbis-1.3.7/lib/pkgconfig/vorbisenc.pc  /opt/lib/pkgconfig/
            cp -f /opt/libvorbis-1.3.7/lib/pkgconfig/vorbisfile.pc /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/libvorbis-1.3.7 && return 0
    else
    
        echo "[Caution] Path: ( /opt/libvorbis-1.3.7 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) libvpx-1.13.0
# ##################################################
function Compile_Install_libvpx_1_13_0() {

    if [[ ! -d "/opt/libvpx-1.13.0" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( libvpx-1.13.0 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/libvpx-1.13.0.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # * Explain: sed -i 's/cp -p/cp/' build/make/Makefile: This command corrects ownership and permissions of installed files.
        #                                                      此命令更正已安装文件的所有权和权限。
        if [[ $STEP_UNZIPPED == 1 ]]; then
            # Install libtheora by running the following commands:
            sed -i 's/cp -p/cp/' $STORAGE/libvpx-1.13.0/build/make/Makefile
        fi
        
        # ------------------------------------------
        # *  Option: --disable-static: This switch prevents installation of static versions of the libraries.
        #                              此选项可防止安装库的静态版本。
        # ..........................................
        # *  Option: --disable-vp8: This switch prevents building of VP8 codec support.
        #                           此选项阻止构建 VP8 编解码器支持。
        # ..........................................
        # *  Option: --disable-vp9: This switch prevents building of VP9 codec support.
        #                           此选项阻止构建 VP9 编解码器支持。
        # ..........................................
        # *  Option: --target=generic-gnu: This switch disables optimizations specific for x86 and x86-64, allowing to build this package without nasm and yasm installed.
        #                                  此选项禁用特定于 x86 和 x86-64 的优化, 允许在不安装 nasm 和 yasm 的情况下构建此包。
        cd $STORAGE/libvpx-1.13.0 && ./configure --prefix=/opt/libvpx-1.13.0 \
                                                 --enable-shared && \
                                                 STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            ln -sf /opt/libvpx-1.13.0/bin/vpxdec /usr/local/bin/
            ln -sf /opt/libvpx-1.13.0/bin/vpxenc /usr/local/bin/
            # ......................................
            rsync -av /opt/libvpx-1.13.0/include/ /usr/local/include/
            rsync -av /opt/libvpx-1.13.0/lib/     /usr/local/lib/
            # ......................................
            cp -f /opt/libvpx-1.13.0/lib/pkgconfig/vpx.pc /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/libvpx-1.13.0 && return 0
    else
    
        echo "[Caution] Path: ( /opt/libvpx-1.13.0 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) x264-20230215
# ##################################################
function Compile_Install_x264_20230215() {

    if [[ ! -d "/opt/x264-20230215" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( x264-20230215 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -xvJf $STORAGE/x264-20230215.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # *  Option: --disable-cli: This switch disables building the command-line encoder which is redundant since it requires FFmpeg for most of the input formats.
        #                           此选项禁止构建命令行编码器, 因为大多数输入格式都需要 FFmpeg, 所以命令行编码器是冗余的。
        # ..........................................
        # *  Option: --disable-asm: Use this switch if you didn't install NASM.
        #                           如果您没有安装 NASM, 请使用此选项。
        cd $STORAGE/x264-20230215 && ./configure --prefix=/opt/x264-20230215 \
                                                 --enable-shared \
                                                 --disable-cli && \
                                                 STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            rsync -av /opt/x264-20230215/include/ /usr/local/include/
            rsync -av /opt/x264-20230215/lib/     /usr/local/lib/
            # ......................................
            cp -f /opt/x264-20230215/lib/pkgconfig/x264.pc /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/x264-20230215 && return 0
    else
    
        echo "[Caution] Path: ( /opt/x264-20230215 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 构建安装(Build Install) x265-20230215
# ##################################################
function Build_Install_x265_20230215() {

    if [[ ! -d "/opt/x265-20230215" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CREATED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( x265-20230215 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -xvJf $STORAGE/x265-20230215.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        mkdir $STORAGE/x265-20230215/my-build && STEP_CREATED=1
        
        # ------------------------------------------
        # *  Option: -DGIT_ARCHETYPE=1: Upstream no longer provides releases. BLFS is using a git snapshot, but if the builder has not installed git the build will not install the shared library or the pkgconfig file without this switch.
        #                               上游不再提供 Releases 版本。BLFS 正在使用 git 快照, 但如果构建器尚未安装 git, 则如果没有此选项, 构建器将不会安装共享库或 pkgconfig 文件。
        # ..........................................
        # *  Option: -Wno-dev: This switch is used to suppress warnings intended for the package's developers.
        #                      此选项用于抑制针对包开发人员的警告。
        cd $STORAGE/x265-20230215/my-build && cmake -G "Unix Makefiles" \
                                                    -DCMAKE_INSTALL_PREFIX=/opt/x265-20230215 \
                                                    -DCMAKE_BUILD_TYPE=Release \
                                                    -DGIT_ARCHETYPE=1 \
                                                    -Wno-dev \
                                                    ../source && STEP_BUILDED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            ln -sf /opt/x265-20230215/bin/x265 /usr/local/bin/
            # ......................................
            rsync -av /opt/x265-20230215/include/ /usr/local/include/
            rsync -av /opt/x265-20230215/lib/     /usr/local/lib/
            # ......................................
            cp -f /opt/x265-20230215/lib/pkgconfig/x265.pc /opt/lib/pkgconfig/
        fi
        
        # ------------------------------------------
        # * Explain: rm -vf /usr/lib/libx265.a: BLFS does not recommend using static libraries.
        #                                       BLFS 不建议使用静态库。
        # ..........................................
        # Now, as the root user:
        # rm -vf /usr/lib/libx265.a 

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/x265-20230215 && return 0
    else
    
        echo "[Caution] Path: ( /opt/x265-20230215 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ########################################### FFmpeg - 6.0 ###########################################

# Function: 编译安装(Compile Install) FFmpeg-6.0
# ##################################################
function Compile_Install_FFmpeg_6_0() {

    if [[ ! -d "/opt/ffmpeg-6.0" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_MADE=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( ffmpeg-6.0 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -xvJf $STORAGE/ffmpeg-6.0.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        if [[ $STEP_UNZIPPED == 1 ]]; then
            # First, apply a patch that adds an API necessary for some packages to build:
            cd $STORAGE/ffmpeg-6.0 && patch -p1 -i ../ffmpeg-6.0-chromium_method-1.patch
            # ......................................
            # Now, apply a patch that allows the package to build with binutils-2.41:
            cd $STORAGE/ffmpeg-6.0 && patch -p1 -i ../ffmpeg-6.0-binutils_2.41-1.patch
        fi
        
        # ------------------------------------------
        # * Default Configure Options:
        #   ./configure --prefix=/usr \
        #               --enable-gpl \
        #               --enable-version3 \
        #               --enable-nonfree \
        #               --disable-static \
        #               --enable-shared \
        #               --disable-debug \
        #               --enable-libaom \
        #               --enable-libass \
        #               --enable-libfdk-aac \
        #               --enable-libfreetype \
        #               --enable-libmp3lame \
        #               --enable-libopus \
        #               --enable-libtheora \
        #               --enable-libvorbis \
        #               --enable-libvpx \
        #               --enable-libx264 \
        #               --enable-libx265 \
        #               --enable-openssl \
        #               --docdir=/usr/share/doc/ffmpeg-6.0
        # ..........................................
        # *  Option: --enable-libfreetype: Enables Freetype support.
        #                                  启用 Freetype 支持。
        # ..........................................
        # *  Option: --enable-gpl: Enables the use of GPL code and permits support for postprocessing, swscale and many other features.
        #                          允许使用 GPL 代码, 并允许支持后处理, swscale 和许多其他功能。
        # ..........................................
        # *  Option: --enable-version3: Enables the use of (L)GPL version 3 code.
        #                               启用(L)GPL 版本 3 代码的使用。
        # ..........................................
        # *  Option: --enable-nonfree: Enables the use of nonfree code. Note that the resulting libraries and binaries will be unredistributable.
        #                              允许使用非自由代码。请注意, 生成的库和二进制文件将是不可分发的。
        # ..........................................
        # *  Option: --disable-static: This switch prevents installation of static versions of the libraries.
        #                              此选项可防止安装库的静态版本。
        # ..........................................
        # *  Option: --enable-shared: Enables building shared libraries, otherwise only static libraries are built and installed.
        #                             启用构建共享库, 否则仅构建和安装静态库。
        # ..........................................
        # *  Option: --disable-debug: Disables building debugging symbols into the programs and libraries.
        #                             禁止在程序和库中生成调试符号。
        # ..........................................
        # *  Option: --enable-libaom: Enables AV1 audio and video decoding via libaom.
        #                             通过 libaom 启用 AV1 音频和视频解码。
        # ..........................................
        # *  Option: --enable-libass: Enables ASS/SSA subtitle format rendering via libass.
        #                             通过 libass 启用 ASS/SSA 字幕格式呈现。
        # ..........................................
        # *  Option: --enable-libdrm: Use this switch if libdrm-2.4.115 is installed to build the “kmsgrab” input module which is useful for screen capturing or streaming.
        #                             如果安装了 libdrm-2.4.115 来构建 "kmsgrab" 输入模块, 则使用此选项, 该模块可用于屏幕捕获或流式传输。
        # ..........................................
        # *  Option: --enable-libfdk-aac: Enables AAC audio encoding via libfdk-aac.
        #                                 通过 libfdk-AAC 启用 AAC 音频编码。
        # ..........................................
        # *  Option: --enable-libmp3lame: Enables MP3 audio encoding via libmp3lame.
        #                                 通过 libmp3lame 启用 MP3 音频编码。
        # ..........................................
        # *  Option: --enable-libvorbis --enable-libtheora: Enables Theora video encoding via libvorbis and libtheora.
        #                                                   通过 libvorbis 和 libtheora 启用 Theora 视频编码。
        # ..........................................
        # *  Option: --enable-libvorbis --enable-libvpx: Enables WebM encoding via libvorbis and libvpx.
        #                                                通过 libvorbis 和 libvpx 启用 WebM 编码。
        # ..........................................
        # *  Option: --enable-libx264: Enables high-quality H.264/MPEG-4 AVC encoding via libx264.
        #                              通过 libx264 实现高质量的 H.264/MPEG-4 AVC 编码。
        # ..........................................
        # *  Option: --enable-libx265: Enables high-quality H.265/HEVC encoding via libx265.
        #                              通过 libx265 实现高质量的 H.265/HEVC 编码。
        # ..........................................
        # *  Option: --enable-openssl: Enables HTTPS protocol for network streams.
        #                              为网络流启用 HTTPS 协议。
        # ..........................................
        # *  Option: --enable-gnutls: Use this option instead of --enable-openssl, if you want to use GnuTLS instead of OpenSSL for HTTPS protocol.
        #                             如果您想在 HTTPS 协议中使用 GnuTLS 而不是 OpenSSL, 请使用此选项, 而不是 --enable-openssl。
        # ..........................................
        # *  Option: --disable-doc: Disables building html documentation. This is only needed if Doxygen-1.9.7 is installed and you do not want to build the html documentation.
        #                           禁用生成 html 文档。只有当安装了 Doxygen-1.9.7 并且您不想构建 html 文档时, 才需要这样做。
        # ..........................................
        # *  Option: --enable-libpulse: Enables support for Pulseaudio for audio output.
        #                               启用对 Pulseaudio 的音频输出支持。
        # ..........................................
        # *  Option: gcc tools/qt-faststart.c -o tools/qt-faststart: This builds the qt-faststart program which can modify QuickTime formatted movies (.mov or .mp4) so that the header information is located at the beginning of the file instead of the end.
        #                                                            This allows the movie file to begin playing before the entire file has been downloaded.
        #                                                            这构建了qt-faststart 程序, 该程序可以修改 QuickTime 格式的电影 (.mov 或 .mp4), 使标题信息位于文件的开头而不是末尾。
        #                                                            这允许在下载整个文件之前开始播放电影文件。
        # ..........................................
        # * Problem: ERROR: libass >= 0.11.0 not found using pkg-config
        #   - Solve: 查看 ffbuild/config.log 在末尾发现:
        #                /opt/libass-0.17.1/lib/libass.so: undefined reference to `fribidi_get_bracket_types'
        #                /opt/libass-0.17.1/lib/libass.so: undefined reference to `fribidi_get_par_embedding_levels_ex'
        #                collect2: error: ld returned 1 exit status
        #            在 ./configure 时, 添加选项 --pkg-config-flags="fribidi" 或者将 fribidi 的 lib 库文件导入查找路径。
        cd $STORAGE/ffmpeg-6.0 && ./configure --prefix=/opt/ffmpeg-6.0 \
                                              --enable-gpl \
                                              --enable-version3 \
                                              --enable-nonfree \
                                              --disable-static \
                                              --enable-shared \
                                              --disable-debug \
                                              --enable-libaom \
                                              --enable-libass \
                                              --enable-libfdk-aac \
                                              --enable-libfreetype \
                                              --enable-libmp3lame \
                                              --enable-libopus \
                                              --enable-libtheora \
                                              --enable-libvorbis \
                                              --enable-libvpx \
                                              --enable-libx264 \
                                              --enable-libx265 \
                                              --enable-openssl \
                                              --pkg-config-flags="fribidi" && \
                                              STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && gcc tools/qt-faststart.c -o tools/qt-faststart && STEP_MADE=1
        
        # ------------------------------------------
        # If you have Doxygen-1.9.7 installed and you wish to build (if --disable-doc was used) or rebuild the html documentation, issue:
        # 如果您安装了 Doxygen-1.9.7, 并且希望构建 (如果使用了--disable-doc) 或重建 html 文档, 请使用:
        # doxygen doc/Doxyfile
        
        # ------------------------------------------
        make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            ln -sf /opt/ffmpeg-6.0/bin/ffmpeg  /usr/local/bin/
            ln -sf /opt/ffmpeg-6.0/bin/ffprobe /usr/local/bin/
            # ......................................
            rsync -av /opt/ffmpeg-6.0/include/ /usr/local/include/
            rsync -av /opt/ffmpeg-6.0/lib/     /usr/local/lib/
            # ......................................
            cp -f /opt/ffmpeg-6.0/lib/pkgconfig/*.pc /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/ffmpeg-6.0 && return 0
    else
    
        echo "[Caution] Path: ( /opt/ffmpeg-6.0 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

function main() {

    # ----------- Compilation Environment ----------
    # 编译 FFmpeg 时, configure 没有专门的 PKG_CONFIG_PATH 选项, 需要导入 PKG_CONFIG_PATH 环境变量。
    export PKG_CONFIG_PATH=/opt/lib/pkgconfig

    # ----------------- Dependency -----------------
    Compile_Install_yasm_1_3_0
    Compile_Install_NASM_2_16_01
    Build_Install_libaom_3_6_1
    Compile_Install_libass_0_17_1
    Compile_Install_fdk_aac_2_0_2
    Compile_Install_LAME_3_100
    Compile_Install_Opus_1_3_1
    Compile_Install_libogg_1_3_5
    Compile_Install_libtheora_1_1_1
    Compile_Install_libvorbis_1_3_7
    Compile_Install_libvpx_1_13_0
    Compile_Install_x264_20230215
    Build_Install_x265_20230215
    # ---------------- FFmpeg - 6.0 ----------------
    Compile_Install_FFmpeg_6_0
}

main
```

## 总结

以上就是关于 Linux运维 Bash脚本 编译安装FFmpeg-6.0 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
