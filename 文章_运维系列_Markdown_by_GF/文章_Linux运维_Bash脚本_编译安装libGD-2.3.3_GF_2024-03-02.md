# 文章_Linux运维_Bash脚本_编译安装libGD-2.3.3_GF_2024-03-02

Bash (Bourne Again Shell) 是一个解释器，负责处理 Unix 系统命令行上的命令。它是由 Brian Fox 编写的免费软件，并于 1989 年发布的免费软件，作为 Sh (Bourne Shell) 的替代品。

您可以在 Linux 和 MacOS 机器上使用 Bash，甚至可以通过适用于 Linux 的 Windows 子系统在 Windows 10 机器上使用。

## 使用方法

* 下载源码包:

gperf-3.1.tar.gz

freetype-2.12.0.tar.gz

expat-2.5.0.tar.gz

fontconfig-2.15.0.tar.xz

libpng-1.6.37.tar.gz

jpegsrc.v9.tar.gz

libgd-2.3.3.tar.xz
  
* 放于指定路径:

这里 Bash Shell 脚本的全局变量 STORAGE 指定的存放源码包的路径 ==/home/goufeng== 可进行修改。
  
* 执行 Bash Shell 脚本:

输入 ==/[路径名]/[脚本名].sh== 即可进行自动编译部署，过程中提示输入 **(y/n)** 输入 **y** 则进行下一步，这样分阶段确认的原因是为了确保能够看到上一个源码编译结果中可能的错误和提示。

## 完整脚本

```shell
#! /bin/bash
# Create By GF 2024-03-01 19:57

# --------------------------------------------------
# Install First:
# * GNU-Tools (Contains: pkg-config, m4, autoconf, automake, libtool, gettext, flex, bison, libiconv, make)

# ------------------- Dependency -------------------
# Need File: gperf-3.1.tar.gz
# Need File: freetype-2.12.0.tar.gz
# Need File: expat-2.5.0.tar.gz
# Need File: fontconfig-2.15.0.tar.xz
# -------------------- Optional --------------------
# Need File: libpng-1.6.37.tar.gz
# Need File: jpegsrc.v9.tar.gz
# --------------------- libGD ----------------------
# Need File: libgd-2.3.3.tar.xz

# ##################################################
STORAGE=/home/goufeng

# ############################################ Dependency ############################################

# Function: 编译安装(Compile Install) gperf-3.1
# ##################################################
function Compile_Install_gperf_3_1() {

    if [[ ! -d "/opt/gperf-3.1" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
        
        # ------------------------------------------
        echo "[Confirm] Compile and Install ( gperf-3.1 )? (y/n)"
        # ..........................................
        read VERIFY
        # ..........................................
        if [[ $VERIFY != "y" ]]; then exit 1; fi
        
        # ------------------------------------------
        tar -zxvf $STORAGE/gperf-3.1.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/gperf-3.1 && ./configure --prefix=/opt/gperf-3.1 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            ln -sf /opt/gperf-3.1/bin/gperf /usr/local/bin/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/gperf-3.1 && return 0
    else
        echo "[Caution] Path: ( /opt/gperf-3.1 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) freetype-2.12.0
# ##################################################
function Compile_Install_freetype_2_12_0() {

    if [[ ! -d "/opt/freetype-2.12.0" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
        
        # ------------------------------------------
        echo "[Confirm] Compile and Install ( freetype-2.12.0 )? (y/n)"
        # ..........................................
        read VERIFY
        # ..........................................
        if [[ $VERIFY != "y" ]]; then exit 1; fi
        
        # ------------------------------------------
        tar -zxvf $STORAGE/freetype-2.12.0.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # * Problem: /usr/bin/ld: //usr/local/lib/libbz2.a(blocksort.o): relocation R_X86_64_PC32 against symbol `stderr@@GLIBC_2.2.5' can not be used when making a shared object; recompile with -fPIC
        #            /usr/bin/ld: final link failed: Bad value
        #            collect2: error: ld returned 1 exit status
        #            config.mk:55: recipe for target '/home/goufeng/freetype-2.12.0/objs/libfreetype.la' failed
        #   - Solve: 在对 bzip2 执行 make 前, 修改 Makefile。
        #                # To assist in cross-compiling
        #                CC=gcc -fPIC # -> 第 1 处修改, 加上 -fPIC。
        #                AR=ar
        #                RANLIB=ranlib
        #                LDFLAGS=
        #                
        #                BIGFILES=-D_FILE_OFFSET_BITS=64
        #                CFLAGS=-Wall -Winline -O2 -fPIC -g $(BIGFILES) # -> 第 2 处修改, 加上 -fPIC。
        #            (第 1 处貌似是外层, 我先是在第 2 处修改后依旧不起作用的时候, 在第 1 处也添加了)
        #            然后进行 make -f Makefile-libbz2_so (在当前目录生成 Shared Library libbz2.so) 或者 make install。
        cd $STORAGE/freetype-2.12.0 && ./configure --prefix=/opt/freetype-2.12.0 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            rsync -av /opt/freetype-2.12.0/include/ /usr/local/include/
            rsync -av /opt/freetype-2.12.0/lib/     /usr/local/lib/
            # ......................................
            cp -f /opt/freetype-2.12.0/lib/pkgconfig/freetype2.pc /opt/lib/pkgconfig/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/freetype-2.12.0 && return 0
    else
        echo "[Caution] Path: ( /opt/freetype-2.12.0 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) expat-2.5.0
# ##################################################
function Compile_Install_expat_2_5_0() {

    if [[ ! -d "/opt/expat-2.5.0" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( expat-2.5.0 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/expat-2.5.0.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/expat-2.5.0 && ./configure --prefix=/opt/expat-2.5.0 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            ln -sf /opt/expat-2.5.0/bin/xmlwf /usr/local/bin/
            # ......................................
            rsync -av /opt/expat-2.5.0/include/ /usr/local/include/
            rsync -av /opt/expat-2.5.0/lib/     /usr/local/lib/
            # ......................................
            cp -f /opt/expat-2.5.0/lib/pkgconfig/expat.pc /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/expat-2.5.0 && return 0
    else
    
        echo "[Caution] Path: ( /opt/expat-2.5.0 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) fontconfig-2.15.0
# ##################################################
function Compile_Install_fontconfig_2_15_0() {

    if [[ ! -d "/opt/fontconfig-2.15.0" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
        
        # ------------------------------------------
        echo "[Confirm] Compile and Install ( fontconfig-2.15.0 )? (y/n)"
        # ..........................................
        read VERIFY
        # ..........................................
        if [[ $VERIFY != "y" ]]; then exit 1; fi
        
        # ------------------------------------------
        tar -xvJf $STORAGE/fontconfig-2.15.0.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/fontconfig-2.15.0 && ./configure --prefix=/opt/fontconfig-2.15.0 \
                                                     PKG_CONFIG_PATH="/opt/lib/pkgconfig" && \
                                                     STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            ln -sf /opt/fontconfig-2.15.0/bin/* /usr/local/bin/
            # ......................................
            rsync -av /opt/fontconfig-2.15.0/include/ /usr/local/include/
            rsync -av /opt/fontconfig-2.15.0/lib/     /usr/local/lib/
            # ......................................
            cp -f /opt/fontconfig-2.15.0/lib/pkgconfig/fontconfig.pc /opt/lib/pkgconfig/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/fontconfig-2.15.0 && return 0
    else
        echo "[Caution] Path: ( /opt/fontconfig-2.15.0 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ############################################# Optional #############################################

# Function: 编译安装(Compile Install) libpng-1.6.37
# ##################################################
function Compile_Install_libpng_1_6_37() {

    if [[ ! -d "/opt/libpng-1.6.37" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
        
        # ------------------------------------------
        echo "[Confirm] Compile and Install ( libpng-1.6.37 )? (y/n)"
        # ..........................................
        read VERIFY
        # ..........................................
        if [[ $VERIFY != "y" ]]; then exit 1; fi
        
        # ------------------------------------------
        tar -zxvf $STORAGE/libpng-1.6.37.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/libpng-1.6.37 && ./configure --prefix=/opt/libpng-1.6.37 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            ln -sf /opt/libpng-1.6.37/bin/* /usr/local/bin/
            # ......................................
            rsync -av /opt/libpng-1.6.37/include/ /usr/local/include/
            rsync -av /opt/libpng-1.6.37/lib/     /usr/local/lib/
            # ......................................
            cp -f /opt/libpng-1.6.37/lib/pkgconfig/libpng16.pc /opt/lib/pkgconfig/
            # ......................................
            ln -sf /opt/lib/pkgconfig/libpng16.pc /opt/lib/pkgconfig/libpng.pc
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/libpng-1.6.37 && return 0
    else
        echo "[Caution] Path: ( /opt/libpng-1.6.37 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) jpeg-9
# ##################################################
function Compile_Install_jpeg_9() {

    if [[ ! -d "/opt/jpeg-9" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
        
        # ------------------------------------------
        echo "[Confirm] Compile and Install ( jpeg-9 )? (y/n)"
        # ..........................................
        read VERIFY
        # ..........................................
        if [[ $VERIFY != "y" ]]; then exit 1; fi
        
        # ------------------------------------------
        tar -zxvf $STORAGE/jpegsrc.v9.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/jpeg-9 && ./configure --prefix=/opt/jpeg-9 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            ln -sf /opt/jpeg-9/bin/* /usr/local/bin/
            # ......................................
            rsync -av /opt/jpeg-9/include/ /usr/local/include/
            rsync -av /opt/jpeg-9/lib/     /usr/local/lib/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/jpeg-9 && return 0
    else
        echo "[Caution] Path: ( /opt/jpeg-9 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ############################################### libGD ##############################################

# Function: 构建安装(Build Install) libgd-2.3.3
# ##################################################
function Compile_Install_libgd_2_3_3() {

    if [[ ! -d "/opt/libgd-2.3.3" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( libgd-2.3.3 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -xvJf $STORAGE/libgd-2.3.3.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/libgd-2.3.3 && ./configure --prefix=/opt/libgd-2.3.3 \
                                               --with-png=/opt/libpng-1.6.37 \
                                               --with-freetype=/opt/freetype-2.12.0 \
                                               --with-fontconfig=/opt/fontconfig-2.15.0 \
                                               --with-jpeg=/opt/jpeg-9 \
                                               PKG_CONFIG_PATH="/opt/lib/pkgconfig" && \
                                               STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            ln -sf /opt/libgd-2.3.3/bin/* /usr/local/bin/
            # ......................................
            rsync -av /opt/libgd-2.3.3/include/ /usr/local/include/
            rsync -av /opt/libgd-2.3.3/lib/     /usr/local/lib/
            # ......................................
            cp -f /opt/libgd-2.3.3/lib/pkgconfig/gdlib.pc /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/libgd-2.3.3 && return 0
    else
    
        echo "[Caution] Path: ( /opt/libgd-2.3.3 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

function main() {

    # ----------------- Dependency -----------------
    Compile_Install_gperf_3_1
    Compile_Install_freetype_2_12_0
    Compile_Install_expat_2_5_0
    Compile_Install_fontconfig_2_15_0
    # ------------------ Optional ------------------
    Compile_Install_libpng_1_6_37
    Compile_Install_jpeg_9
    # ------------------- libGD --------------------
    Compile_Install_libgd_2_3_3
}

main
```

## 总结

以上就是关于 Linux运维 Bash脚本 编译安装libGD-2.3.3 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
